from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from DB.models import User_Create, User, User_Response, Session_Record
from sqlmodel import Session, select
from DB.db_config import get_db
from .password import hash_pass, verify_pass, set_cookie_helper, get_cookie_helper
import secrets
import hashlib
from datetime import datetime, timezone, timedelta

route = APIRouter(prefix="/session-auth", tags=["Session Base Auth"])

@route.post("", response_model=User_Response, status_code=status.HTTP_201_CREATED)
def create_user(user: User_Create, response:Response, session:Session = Depends(get_db)):

    username, password = user.username, user.password
    username = str(username).strip()
    password = str(password).strip()
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

    session_id = secrets.token_urlsafe(32)
    session_id_hash=hashlib.sha256(session_id.encode()).hexdigest()
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(hours=1)

    session_data = Session_Record(session_id=session_id_hash, user_id=data.id, created_at=now, last_activity_at=now, expires_at = expires_at)
    session.add(session_data)
    session.commit()
    session.refresh(data)
    set_cookie_helper("session_id", session_id, response, 3600)

    return User_Response(id=data.id, username=data.username)


@route.get("", status_code=status.HTTP_200_OK)
def get_user(request: Request, session:Session= Depends(get_db)):
    cookies_data = get_cookie_helper("session_id", request)
    cookies_data_hash = hashlib.sha256(cookies_data.encode()).hexdigest()

    query = select(Session_Record).where(Session_Record.session_id==cookies_data_hash)
    record = session.exec(query).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have not this permission"
        )
    if record.expires_at <= datetime.now(timezone.utc):
        record.is_active = False
        session.commit()
    
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired"
        )
    if not record.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have not this permission"
        )
    user_query = select(User).where(User.id==record.user_id)
    user = session.exec(user_query).first()
    if not user:
        record.is_active = False
        session.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have not this permission"
        )
    record.last_activity_at=datetime.now(timezone.utc)
    session.commit()
    return User_Response(id=user.id, username=user.username)

@route.post("/login", status_code=status.HTTP_201_CREATED)
def get_login(user: User_Create, response: Response, session:Session= Depends(get_db)):
    username, password = user.username.strip(), user.password

    user_query = select(User).where(User.username==username)
    user = session.exec(user_query).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please Sign up first"
        )
    if not verify_pass(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    query = select(Session_Record).where(Session_Record.user_id==user.id, Session_Record.is_active==True)
    record = session.exec(query).first()
    if record:
        record.is_active=False
    
    session_id = secrets.token_urlsafe(32)
    session_id_hash=hashlib.sha256(session_id.encode()).hexdigest()
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(hours=1)

    session_data = Session_Record(session_id=session_id_hash, user_id=user.id, created_at=now, last_activity_at=now, expires_at = expires_at)
    session.add(session_data)
    session.commit()
    set_cookie_helper("session_id", session_id, response, 3600)

    return User_Response(id=user.id, username=user.username)


