import bcrypt
from fastapi import Response, Request, HTTPException, status
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timezone, timedelta

load_dotenv()

isProd = bool(os.getenv("IsProduction"))
jwt_secrate = os.getenv("JWT_SECRET_KEY")
jwt_algo = os.getenv("JWT_ALGORITHM")
jwt_token_time = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def hash_pass(password: str) -> str:
    pass_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(pass_bytes, salt)
    return hashed.decode("utf-8")

def verify_pass(plain_pass:str, hashed_pass:str)->bool:
    return bcrypt.checkpw(plain_pass.encode("utf-8"), hashed_pass.encode("utf-8"))

def set_cookie_helper(cookie_key: str, cookie_data:str, response: Response, max_age: int):
    response.set_cookie(
        key=cookie_key,
        value=cookie_data,
        httponly=True,
        secure=isProd,
        samesite="lax",
        max_age=max_age, #in sec
        path="/"
    )

def get_cookie_helper(cookie_key: str, request: Request)->str:
    cookie_data = request.cookies.get(cookie_key)
    if not cookie_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have not this permission"
        )
    return cookie_data.strip()


def create_jwt(user_id: int)->str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=jwt_token_time
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    token = jwt.encode(
        payload,
        jwt_secrate,
        algorithm=jwt_algo
    )

    return token

