from pydantic import BaseModel
import httpx
from hashlib import sha1


class UserInformation(BaseModel):
    login: str
    password: str


def register_user(login: str, password: str):
    user_info = UserInformation(login=login, password=sha1(password.encode()).hexdigest())
    response = httpx.post("http://127.0.0.1:8000//auth/sign-up", json=user_info.dict())
    return response


def login_user(login, password):
    user_info = UserInformation(login=login, password=sha1(password.encode()).hexdigest())
    response = httpx.post("http://127.0.0.1:8000/auth/sign-in", json=user_info.dict())
    return response
