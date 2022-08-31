from typing import Optional

from database.connection import Base
from pydantic import BaseModel
from sqlalchemy.orm import Session


def set_model_attrs(
    model: Base, schema: Optional[BaseModel], meta: Optional[dict]
) -> None:
    if schema:
        for name, value in schema.dict().items():
            setattr(model, name, value)
    if meta:
        for name, value in meta.items():
            setattr(model, name, value)


def encode_password(password: str) -> str:
    result = "anoni_hash:"
    return result + password


def save_model(model: Base, db: Session) -> None:
    db.add(model)
    db.commit()
    db.refresh(model)
