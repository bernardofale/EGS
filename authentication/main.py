from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from pydantic import BaseModel
import base64
import requests

DATABASE_URL = "mysql+mysqlconnector://root:password@auth_db/auth"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)  # Mudei isto (Nuno) atribui um valor especifico pq estav a dar erro
    email = Column(String(120), unique=True)    # Mudei isto (Nuno) atribui um valor especifico pq estav a dar erro
    provider = Column(String(50))  # Mudei isto (Nuno) atribui um valor especifico pq estav a dar erro

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_user_login_status(db, access_token):
    return db.query(User).filter(User.access_token == access_token).first()

def validate_access_token(access_token, provider):
    if provider == 'github':
        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.get("https://api.github.com/user", headers=headers)
        return response.status_code == 200
    elif provider == 'ua':
        # Implement token validation logic for UA provider
        pass
    return False

def register_user(db, email, access_token, provider):
    user = User(email=email, access_token=access_token, provider=provider)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

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

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

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
async def callback_ua(code: str, db: Session = Depends(get_db)):
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
        db.add(User(email="example@example.com", access_token=access_token, provider='ua'))
        db.commit()
        
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to obtain access token")

@app.get("/callback/github")
async def callback_github(code: str, db: Session = Depends(get_db)):
    client_id = "ed07148229986602e861"
    client_secret = "5d7e5a7849a396f44c2dfd4cc59bf490fed0348b"
    redirect_uri = "http://localhost:8000/index"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    headers = {"Accept": "application/json"}
    response = requests.post("https://github.com/login/oauth/access_token", data=data, headers=headers)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")

        # Fetch user details
        headers = {"Authorization": f"token {access_token}"}
        user_response = requests.get("https://api.github.com/user", headers=headers)
        user_data = user_response.json()
        
        # Store user information in the database
        email = user_data.get('email', f"{user_data['login']}@github.com")  # Handle cases where email is not provided
        user = db.query(User).filter(User.email == email).first()
        if not user:
            db.add(User(email=email, access_token=access_token, provider='github'))
            db.commit()
        
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to obtain access token")

@app.get("/authVeri")
async def authenticate_user(access_token: str = Depends(oauth2_scheme_ua), db: Session = Depends(get_db)):
    user = check_user_login_status(db, access_token)
    if user:
        return {"message": "Welcome to the homepage!", "user_id": user.id}
    else:
        return {"message": "Please register"}

@app.post("/register")
async def register_user_endpoint(email: str, access_token: str, provider: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return {"message": "User already exists"}
    user = register_user(db, email, access_token, provider)
    return {"message": "User registered successfully", "user_id": user.id}

@app.get("/token/validate")
async def validate_token(access_token: str, provider: str):
    if validate_access_token(access_token, provider):
        return {"message": "Token is valid"}
    else:
        return {"message": "Token is invalid"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
