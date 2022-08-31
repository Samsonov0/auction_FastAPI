from database.connection import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from user.models import User
from user.utils import encode_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(tags=["authentication"])


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = encode_password(form_data.password)
    if hashed_password != user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.id, "token_type": "bearer"}


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
