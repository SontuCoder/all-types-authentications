from fastapi import APIRouter, Depends, HTTPException, status, Request
from DB.models import User_Create, User, User_Response
from sqlmodel import Session, select
from DB.db_config import get_db
from .password import hash_pass, verify_pass
import base64
import binascii

route = APIRouter(prefix="/basic-auth", tags=["Basic Auth"])

@route.post("", response_model=User_Response, status_code=status.HTTP_201_CREATED)
def create_user(user: User_Create, session: Session = Depends(get_db)):
    query = select(User).where(User.username==user.username)
    result=session.exec(query).all()
    if len(result):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist with this username"
        )
    
    user.username = str(user.username).strip()
    user.password = str(user.password).strip()
    user.password = hash_pass(user.password)

    data = User(username=user.username, password=user.password)
    session.add(data)
    session.commit()
    session.refresh(data)
    
    return User_Response(id=data.id, username=data.username)


@route.get("", response_model=User_Response)
def get_user_details(request:Request, session:Session = Depends(get_db)):
    header_details = request.headers.get("authorization")

    if not header_details:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong header details"
        )
    if len(header_details.split(" ")) != 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong header details"
        )
    if not header_details.split(" ")[1].strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong header details"
        )
    scheme, credentials = header_details.split(" ", 1)

    if scheme.lower() != "basic":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong header details"
        )
    try:
        decoded = base64.b64decode(
            credentials,
            validate=True
        ).decode("utf-8")
    
        username, password = decoded.split(":", 1)
    except (binascii.Error, UnicodeDecodeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    query = select(User).where(User.username==username.strip())
    user=session.exec(query).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not exist with this username"
        )
    if not verify_pass(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong credentials"
        )
    return User_Response(id=user.id, username=user.username)

