from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import uuid4
from datetime import datetime, timedelta

app = FastAPI()

# Secret key to sign JWT tokens (this should be kept secure in production)
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Fake user data for demonstration purposes
fake_users_db = {
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": "fakehashedpassword",
        "is_admin": True,
    },
    "testuser": {
        "username": "testuser",
        "email": "testuser@example.com",
        "hashed_password": "fakehashedpassword",
        "is_admin": False,
    },
}

# Fake tokens for demonstration purposes
fake_refresh_tokens = {}

# Model for JWT token
class Token(BaseModel):
    access_token: str
    token_type: str

# Model for user input during registration
class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str

# Model for user input during login
class UserLogin(BaseModel):
    username: str
    password: str

# OAuth2PasswordBearer is used for handling token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to create JWT token
def create_jwt_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default token expiration

    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Function to get user information from the token
def get_user_info(token: str = Depends(oauth2_scheme)):
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

    return fake_users_db[username]

# Registration endpoint
@app.post("/register", response_model=Token)
async def register(user_data: UserRegistration):
    if user_data.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    if user_data.email in [u["email"] for u in fake_users_db.values()]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Hash the password (you should use a secure method in production)
    hashed_password = user_data.password + "_hashed"

    # Store user data (in-memory for simplicity)
    fake_users_db[user_data.username] = {
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hashed_password,
        "is_admin": False,
    }

    # Create and return JWT token for immediate login
    token_data = {"sub": user_data.username}
    access_token = create_jwt_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}

# Login endpoint
@app.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    user = fake_users_db.get(user_data.username)
    if user is None or user["hashed_password"] != user_data.password + "_hashed":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create and return JWT token for authentication
    token_data = {"sub": user_data.username}
    access_token = create_jwt_token(token_data)
    refresh_token = str(uuid4())
    fake_refresh_tokens[refresh_token] = user_data.username

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

# Token refresh endpoint
@app.post("/refresh-token", response_model=Token)
async def refresh_token(refresh_token: str):
    if refresh_token not in fake_refresh_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    username = fake_refresh_tokens[refresh_token]

    # Create and return new JWT token for authentication
    token_data = {"sub": username}
    access_token = create_jwt_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}

# Logout endpoint
@app.post("/logout")
async def logout(refresh_token: str):
    if refresh_token in fake_refresh_tokens:
        del fake_refresh_tokens[refresh_token]
    return {"message": "Logout successful"}

# Password reset endpoints
@app.post("/forgot-password")
async def forgot_password(email: EmailStr):
    # Implement logic to send a password reset email to the user
    # In a real-world scenario, you would generate a token and send a link with the token
    # For simplicity, we will just return a message here
    return {"message": f"Password reset email sent to {email}"}

@app.post("/reset-password")
async def reset_password(token: str, new_password: str):
    # Implement logic to validate the reset token and update the user's password
    # In a real-world scenario, you would verify the token and update the password in the database
    # For simplicity, we will just return a message here
    return {"message": "Password reset successful"}

# Email verification endpoints
@app.post("/send-verification-email")
async def send_verification_email(email: EmailStr):
    # Implement logic to send an email with a verification link to the user
    # In a real-world scenario, you would generate a token and send a link with the token
    # For simplicity, we will just return a message here
    return {"message": f"Verification email sent to {email}"}

@app.post("/verify-email")
async def verify_email(token: str):
    # Implement logic to verify the email using the provided token
    # In a real-world scenario, you would verify the token and update the email verification status in the database
    # For simplicity, we will just return a message here
    return {"message": "Email verification successful"}

# Endpoint to retrieve user profile
@app.get("/profile", response_model=dict)
async def profile(user: dict = Depends(get_user_info)):
    return user

# Endpoint to change password (requires authentication)
@app.patch("/change-password")
async def change_password(new_password: str, user: dict = Depends(get_user_info)):
    # Update the password in the fake user database (you should use a secure method in production)
    fake_users_db[user["username"]]["hashed_password"] = new_password + "_hashed"
    return {"message": "Password changed successfully"}

# Endpoint to deactivate account (requires authentication)
@app.delete("/deactivate-account")
async def deactivate_account(user: dict = Depends(get_user_info)):
    # Remove the user from the fake user database (you should implement proper account deactivation in production)
    del fake_users_db[user["username"]]
    return {"message": "Account deactivated successfully"}

# Example route that requires admin privileges (requires authentication)
@app.get("/users", response_model=List[dict])
async def get_users(user: dict = Depends(get_user_info)):
    if not user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have admin privileges",
        )

    # Return a list of users (excluding hashed passwords)
    return [
        {"username": u["username"], "email": u["email"], "is_admin": u["is_admin"]}
        for u in fake_users_db.values()
    ]