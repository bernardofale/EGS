from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI()

# Secret key to sign JWT tokens
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Example user model, replace it with your actual user model
class User(BaseModel):
    username: str
    email: str
    hashed_password: str

# Example user data store, replace it with your actual data store
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "email": "testuser@example.com",
        "hashed_password": "fakehashedpassword",
    }
}

# OAuth2 password bearer for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to create JWT tokens
def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to get current user from token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    if username not in fake_users_db:
        raise credentials_exception
    return User(**fake_users_db[username])

# Models for request and response payloads
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ProfileResponse(BaseModel):
    username: str
    email: str

class UpdateProfileRequest(BaseModel):
    email: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

# Endpoint to register a new user
@app.post("/register")
async def register(user: RegisterRequest):
    # Logic for user registration (validate, hash password, save to database, etc.)
    # For simplicity, using a fake database in this example
    fake_users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "hashed_password": "fakehashedpassword",
    }
    return {"message": "User registered successfully"}

# Endpoint to authenticate and generate a token
@app.post("/login", response_model=Token)
async def login(user: LoginRequest):
    # Logic for user authentication (validate credentials, generate token, etc.)
    # For simplicity, using a fake database in this example
    if user.username in fake_users_db and fake_users_db[user.username]["hashed_password"] == "fakehashedpassword":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_jwt_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

# Endpoint to retrieve user profile
@app.get("/profile", response_model=ProfileResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user.dict()

# Endpoint to update user profile
@app.put("/profile", response_model=dict)
async def update_profile(update_data: UpdateProfileRequest, current_user: User = Depends(get_current_user)):
    # Logic for updating user profile (validate, update database, etc.)
    # For simplicity, using a fake database in this example
    if update_data.email:
        current_user.email = update_data.email
    return {"message": "Profile updated successfully"}

# Endpoint to delete user account
@app.delete("/profile", response_model=dict)
async def delete_profile(current_user: User = Depends(get_current_user)):
    # Logic for deleting user account (delete from database, invalidate tokens, etc.)
    # For simplicity, using a fake database in this example
    del fake_users_db[current_user.username]
    return {"message": "Account deleted successfully"}

# Endpoint to logout and invalidate token
@app.post("/logout", response_model=dict)
async def logout():
    # Logic for logging out (invalidate token, remove session data, etc.)
    return {"message": "Logged out successfully"}

# Endpoint to request password reset
@app.post("/reset-password", response_model=dict)
async def request_password_reset(user_identifier: str):
    # Logic for sending password reset instructions (generate token, send email, etc.)
    # For simplicity, not implementing the actual password reset functionality in this example
    return {"message": "Password reset instructions sent"}

# Endpoint to perform password reset
@app.put("/reset-password", response_model=dict)
async def reset_password(new_password: str, reset_token: str):
    # Logic for resetting the user's password (validate token, update password, etc.)
    # For simplicity, not implementing the actual password reset functionality in this example
    return {"message": "Password reset successfully"}

# Endpoint to change user password
@app.patch("/change-password", response_model=dict)
async def change_password(password_data: ChangePasswordRequest, current_user: User = Depends(get_current_user)):
    # Logic for changing user password (validate, update database, etc.)
    # For simplicity, using a fake database in this example
    if fake_users_db[current_user.username]["hashed_password"] == "fakehashedpassword":
        fake_users_db[current_user.username]["hashed_password"] = "newfakehashedpassword"
        return {"message": "Password changed successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to change password")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
