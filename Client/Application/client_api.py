from pydantic import BaseModel
import httpx
from hashlib import sha256


class UserInformation(BaseModel):
    login: str
    password: str
    user_id: str | None


class UserGetMusic(BaseModel):
    user_id: int
    style_music: list
    music_length: int = 5  # ["angry","dark"]


def register_user(login: str, password: str):
    user_info = UserInformation(login=login, password=sha256(password.encode()).hexdigest(), user_id=None)
    response = httpx.post("http://127.0.0.1:8000/auth/sign-up", json=user_info.dict())
    return response.json()


def login_user(login: str, password: str, user_id: str):
    user_info = UserInformation(login=login, password=sha256(password.encode()).hexdigest(), user_id=user_id)
    response = httpx.post("http://127.0.0.1:8000/auth/sign-in", json=user_info.dict())
    return response.json()


def get_music():
    user_get_music = UserGetMusic(user_id="", style_music=["angry", "dark"],)
    response = httpx.post("http://127.0.0.1:8000/get_music", json=user_get_music.dict())

