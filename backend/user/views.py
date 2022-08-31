from database.connection import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from user.authentication_logic import get_current_user
from user.models import User
from user.schemas import (
    CreateUserSchema,
    ErrorMessage,
    GetUserWithIdSchema,
    SuccessMessage,
    UpdateUserSchema,
)
from user.utils import encode_password, save_model, set_model_attrs
from user.validation import validate_create_user

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/register",
    responses={201: {"model": SuccessMessage}, 400: {"model": ErrorMessage}},
)
def register(user_schema: CreateUserSchema, db: Session = Depends(get_db)):
    is_valid, text = validate_create_user(db, user_schema)

    if not is_valid:
        return JSONResponse(
            {"message": text, "success": False}, status_code=status.HTTP_400_BAD_REQUEST
        )

    user = User()
    password = encode_password(user_schema.password)
    set_model_attrs(model=user, schema=user_schema, meta={"password": password})
    save_model(user, db)

    return JSONResponse(
        {"message": "user created. enjoy the games", "success": True},
        status_code=status.HTTP_201_CREATED,
    )


@router.post("/edit/me", responses={200: {"model": SuccessMessage}})
def edit_user(
    user_schema: UpdateUserSchema,
    db: Session = Depends(get_db),
    this_user: GetUserWithIdSchema = Depends(get_current_user),
):
    if db.query(User).filter(User.email == user_schema.email).first():
        return JSONResponse({"message": "this email zanat"})

    user = db.query(User).filter(User.id == this_user.id).first()
    set_model_attrs(model=user, schema=user_schema, meta=None)
    db.commit()
    return JSONResponse(
        {"message": "user has been updated", "success": True},
        status_code=status.HTTP_200_OK,
    )
