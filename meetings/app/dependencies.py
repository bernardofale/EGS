from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

API_KEY = 'o3e17a9d25945d0d7d009ccd62a5a7816265d3c6ffa03334a85cfd74be10c55e7'
HELLOSIGN_API_KEY = 'o878dfbff49eceb3431c5b405b8e318117418efd536c9f0a0cd8881ed13b305db'
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
