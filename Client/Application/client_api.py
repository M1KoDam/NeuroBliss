from pydantic import BaseModel
import httpx
from hashlib import sha256


class UserInformation(BaseModel):
    login: str
    password: str


def register_user(login: str, password: str):
    user_info = UserInformation(login=login, password=sha256(password.encode()).hexdigest())
    response = httpx.post("http://127.0.0.1:8000/auth/sign-up", json=user_info.dict())
    return response.json()


def login_user(login: str, password: str):
    user_info = UserInformation(login=login, password=sha256(password.encode()).hexdigest())
    response = httpx.post("http://127.0.0.1:8000/auth/sign-in", json=user_info.dict())
    return response.json()
