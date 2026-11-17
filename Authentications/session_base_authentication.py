from fastapi import APIRouter, Depends, HTTPException, status, Request
from DB.models import User_Create, User, User_Response, Session_Record
from sqlmodel import Session, select
from DB.db_config import get_db
from .password import hash_pass, verify_pass
import secrets

route = APIRouter(prefix="/session-auth", tags=["Session Base Auth"])

@route.post("", response_model=User_Response, status_code=status.HTTP_201_CREATED)
def create_user(user: User_Create, session:Session = Depends(get_db)):
    username, password = user.username, user.password
    query = select(User).where(User.username==username)
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

    session_id = secrets.token_urlsafe(32)
    session_data = Session_Record(session_id=session_id, user_id=data.id)
    session.add(session_data)
    session.commit()
    session.refresh(session_data)
    
