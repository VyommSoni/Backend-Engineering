"""stateless authenticaion --JWT (json web token) based authentication module for the application.

 why need?
 
 In Session based authentication, the server needs to maintain the state of the user across multiple requests, which can lead to scalability issues. In contrast, stateless authentication allows the server to authenticate users without storing any session information on the server side. Instead, the server generates a token (JWT) that contains user information and sends it to the client. The client includes this token in subsequent requests, allowing the server to verify the user's identity without maintaining any session state.
 
 By using JWT we solve the issues of scalability and performance
 
 how it works?
 
 users logs in with their credentials, the server validates the credentials and generates a JWT containing user information (like user ID, role, etc.) and a signature. The server sends this token back to the client, which stores it (usually in local storage or cookies). For subsequent requests, the client includes the JWT in the Authorization header. The server verifies the token's signature and extracts user information from it, allowing the server to authenticate the user without maintaining any session state."""


from pydantic import BaseModel

from fastapi import FastAPI, Request, Response, HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, Optional
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

SECRET_KEY = "super-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app=FastAPI(title="Stateless Authentication")
class UserLogin(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "alice": {
        "username": "alice",
        "hashed_password": pwd_context.hash("secretpassword"),
        "role": "admin",
    },
    "bob": {
        "username": "bob",
        "hashed_password": pwd_context.hash("password123"),
        "role": "user",
    },
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/jwt/login")

@app.post("/auth/jwt/login", response_model=Token)
def login_jwt(form_data: UserLogin):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(
        form_data.password, user["hashed_password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # Create stateless JWT token containing claims
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user_jwt(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> dict:
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
    except jwt.PyJWTError:
        raise credentials_exception

    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return user


@app.get("/profile/jwt")
def jwt_protected_route(
    current_user: Annotated[dict, Depends(get_current_user_jwt)]
):
    return {
        "auth_type": "JWT Bearer Token",
        "user": current_user["username"],
        "role": current_user["role"],
    }




