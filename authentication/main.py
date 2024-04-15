from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
import base64
import requests


app = FastAPI()
oauth2_scheme_ua = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://wso2-gw.ua.pt/authorize",
    tokenUrl="https://wso2-gw.ua.pt/token",
    scopes={"openid": "OpenID authentication"}
)
oauth2_scheme_github = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://github.com/login/oauth/authorize",
    tokenUrl="https://github.com/login/oauth/access_token",
    scopes={"user": "User details"}
)

DATABASE_URL = "mysql+mysqlconnector://root:password@localhost:3307/auth"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True, index=True)
    access_token = Column(String)
    provider = Column(String)

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def index():
    return {"message": "Welcome to the index page"}

@app.get("/index")
async def main():
    return {"Congratulations, your authentication was valid"}

@app.get("/signin/ua")
async def signin():
    redirect_uri = "http://localhost:5000"
    client_id = "agh44RajMJcYvCIq3lSMrutfPJ0a"
    state = "1234567890"
    scope = "openid"
    authorization_url = f"https://wso2-gw.ua.pt/authorize?response_type=code&client_id={client_id}&state={state}&scope={scope}&redirect_uri={redirect_uri}"
    return RedirectResponse(url=authorization_url)

@app.get("/signin/github")
async def signin_github():
    redirect_uri = "http://localhost:8000/index"
    client_id = "ed07148229986602e861"
    state = "1234567890"
    scope = "user"
    authorization_url = f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&state={state}&scope={scope}"
    return RedirectResponse(url=authorization_url)

@app.get("/callback/ua")
async def callback_ua(code: str):
    client_id = "agh44RajMJcYvCIq3lSMrutfPJ0a"
    client_secret = "WJckU0FSb41rsJHLnFPYqBFvSZoa"
    redirect_uri = "http://localhost:5000"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"
    }
    response = requests.post("https://wso2-gw.ua.pt/token", data=data, headers=headers)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        token_type = token_data.get("token_type")
        
        # Store user information in the database
        db = SessionLocal()
        db.add(User(email="dummy@example.com", access_token=access_token, refresh_token=refresh_token))
        db.commit()
        db.close()
        
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to obtain access token")

@app.get("/callback/github")
async def callback_github(code: str):
    client_id = "ed07148229986602e861"
    client_secret = "5d7e5a7849a396f44c2dfd4cc59bf490fed0348b"
    redirect_uri = "http://localhost:8000/index"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    response = requests.post("https://github.com/login/oauth/access_token", data=data)
    if response.status_code == 200:
        token_data = response.text
        access_token = token_data.split("=")[1].split("&")[0]
        
        # Fetch user details
        headers = {"Authorization": f"token {access_token}"}
        user_response = requests.get("https://api.github.com/user", headers=headers)
        user_data = user_response.json()
        
        # Store user information in the database
        db = SessionLocal()
        db.add(User(email=user_data['email'], access_token=access_token, provider='github'))
        db.commit()
        db.close()
        
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to obtain access token")

@app.get("/authVeri")
async def register(access_token: str = Depends(oauth2_scheme_ua)):
    # Check if the user is already in the database
    db = SessionLocal()
    user = db.query(User).filter(User.access_token == access_token).first()
    db.close()

    if user:
        return {"message": "Welcome to the homepage!"}
    else:
        return {"message": "Please register"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
