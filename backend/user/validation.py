import re

from pydantic import BaseModel
from user.models import User


def validate_create_user(db, schema: BaseModel):
    valid_name = re.compile(r"^[a-z0-9]+$", re.I)
    valid_email = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    user = db.query(User).filter(User.email == schema.email).first()
    user_by_username = db.query(User).filter(User.username == schema.username).first()
    if user:
        return False, f"user with '{schema.email}' email has been exists"
    if user_by_username:
        return False, f"user with '{schema.username}' username has been exists"
    if not valid_name.match(schema.username):
        return (
            False,
            "wrong username. please use only numbers from 0 to 9 and only letters from a to z.",
        )
    if not valid_email.match(schema.email):
        return False, "wrong email"
    if len(schema.username) > 50:
        return False, "please use a shorter username"
    if len(schema.name) > 30:
        return False, "please use a shorter name"
    if len(schema.last_name) > 35:
        return False, "please use a shorter last name"
    if len(schema.patronymic) > 35:
        return False, "please use a shorter patronymic"
    if len(schema.password) > 50:
        return False, "please use a shorter password"
    return True, ""
