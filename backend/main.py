import base64
import binascii

from auction.views import router as auction_router
from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from settings import Settings
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
)
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from user.authentication_logic import router as authentication_router
from user.views import router as user_router


@AuthJWT.load_config
def get_config():
    return Settings()


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != "basic":
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError("Invalid basic auth credentials")

        username, _, password = decoded.partition(":")
        # TODO: You'd want to verify the username and password here.
        return AuthCredentials(["authenticated"]), SimpleUser(username)


middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend()),
]


app = FastAPI(middleware=middleware)
app.include_router(authentication_router)

app.include_router(user_router)
app.include_router(auction_router)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.middleware("http")
async def create_cose(request: Request, call_next):
    response = await call_next(request)
    response.headers["user"] = "123"
    return response
