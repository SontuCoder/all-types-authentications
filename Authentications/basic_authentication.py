from fastapi import APIRouter, Depends, HTTPException, status
from DB.models import User_Create, User, User_Response
from sqlmodel import Session, select
from DB.db_config import get_db
from password import hash_pass, verify_pass

route = APIRouter(prefix="/basic-auth", tags=["Basic Auth"])


@route.post("", response_model=User_Response)
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
    data = User(**user)
    session.add(data)
    session.commit()
    session.refresh(data)
    
    return User_Response(id=data.id, username=data.username)


