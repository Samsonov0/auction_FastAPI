from typing import Optional

from pydantic import BaseModel


class BaseUserSchema(BaseModel):
    username: str
    name: str
    last_name: str
    patronymic: str


class CreateUserSchema(BaseUserSchema):
    password: str
    email: str

    class Config:
        orm_mode = True


class GetUserWithIdSchema(BaseUserSchema):
    id: int


class UpdateUserSchema(BaseUserSchema):
    email: str


class SuccessMessage(BaseModel):
    id: int
    message: Optional[str]
    success: bool = True


class ErrorMessage(BaseModel):
    message: str
    success: bool = False


class AuthSchema(BaseModel):
    email: str
    password: str
