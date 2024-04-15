from fastapi import Header, HTTPException
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")


async def verify_key(authorization: str = Header(None)):
    if authorization != API_KEY:
        raise HTTPException(status_code=401, detail="ERROR: Invalid key")
    elif authorization is None:
        raise HTTPException(status_code=401, detail="ERROR: No key provided")
    return authorization
