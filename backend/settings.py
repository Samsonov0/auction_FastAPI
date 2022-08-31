from pydantic import BaseModel


class Settings(BaseModel):
    """
    Здесь располагаются переменные необходимые для работы приложения
    """

    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False
