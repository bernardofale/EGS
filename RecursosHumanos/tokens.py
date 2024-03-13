from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.models import Token, User, UserInDB
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "ricaxe.ua"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

users_db = []

# Função para criar um token de acesso
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Rota de registro para criar usuários
@app.post("/register/", response_model=Token)
async def register_user(user: User):
    # Simulação de armazenamento seguro da senha (você deve usar hashing em um ambiente real)
    hashed_password = user.password + "_hashed"
    user_in_db = UserInDB(**user.dict(), hashed_password=hashed_password)
    users_db.append(user_in_db)
    
    # Criar token de acesso ao registrar
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Função para obter usuário pelo nome de usuário
def get_user(username: str):
    for user in users_db:
        if user.username == username:
            return user

# Função para autenticar usuários
async def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or password + "_hashed" != user.hashed_password:
        return None
    return user

# Função para obter usuário atual a partir do token de acesso
async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

# Rota para obter informações do usuário autenticado
@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user