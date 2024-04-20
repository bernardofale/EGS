from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
HELLOSIGN_API_KEY = os.getenv("HELLOSIGN_KEY")
security = HTTPBearer()


async def verify_key(credentials: HTTPAuthorizationCredentials
                     = Depends(security)):
    key = credentials.credentials
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="ERROR: Invalid key")
    elif key is None:
        raise HTTPException(status_code=401, detail="ERROR: No key provided")
    return key


async def get_hello_sign_key():
    return HELLOSIGN_API_KEY
