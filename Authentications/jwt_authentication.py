from fastapi import APIRouter, Depends, HTTPException, status, Request
from DB.models import User_Create, User, User_Response, User_JWT_Response
from sqlmodel import Session, select
from DB.db_config import get_db
from .password import hash_pass, verify_pass

route = APIRouter(prefix="/jwt-auth", tags=["JWT Auth"])

@route.post("", response_model=User_JWT_Response, status_code=status.HTTP_201_CREATED)
def get_register(user:User_Create, session: Session=Depends(get_db)):
    username, password=user.username.strip(), user.password

    query = select(User).where(User.username==username)
    result=session.exec(query).first()
    if result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist with this username"
        )
    password = hash_pass(password)

    data = User(username=username, password=password)
    session.add(data)
    session.flush()

    