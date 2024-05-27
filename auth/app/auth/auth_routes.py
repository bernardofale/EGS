from fastapi import APIRouter, Depends, Response, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.crud.crud_ops import insert_user, get_user, authenticate_user
from app.resp_models.model import Token, UserInDB, User
from app.auth.gen_tokens import create_access_token
from app.auth.gen_tokens import oauth2_scheme, TokenData
from jose import jwt, JWTError
from datetime import timedelta


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
JWT_EXPIRY = 30
JWT_SECRET = "48dd53b11f29fe0aceeb80a83b921b9fda93974121546cd8400eac7c2cc27c41"
JWT_ALGORITHM = "HS256"


@router.get("/verify")
async def verify_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return User(**(user.dict()))


@router.post("/", response_model=Token)
async def login(response: Response,
                form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(JWT_EXPIRY))
    token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value = token.access_token, httponly=True, secure=True)
    return token

@router.post("/register", )
def register(user : UserInDB):
    return insert_user(user)
