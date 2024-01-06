from pydantic import BaseModel
import httpx
from hashlib import sha256


class UserInformation(BaseModel):
    login: str
    password: str
    user_id: str | None


class UserGetMusic(BaseModel):
    user_id: str
    style_music: list
    music_length: int = 5  # ["angry","dark"]


class MusicInfo(BaseModel):
    music_id: str
    user_id: str


def register_user(login: str, password: str):
    user_info = UserInformation(login=login, password=sha256(password.encode()).hexdigest(), user_id=None)
    response = httpx.post("http://127.0.0.1:8000/auth/sign-up", json=user_info.dict())
    return response.json()


def login_user(login: str, password: str, user_id: str):
    user_info = UserInformation(login=login, password=sha256(password.encode()).hexdigest(), user_id=user_id)
    response = httpx.post("http://127.0.0.1:8000/auth/sign-in", json=user_info.dict())
    return response.json()


def get_music_generation(user_id: str, style_music: list):
    user_get_music = UserGetMusic(user_id=user_id, style_music=style_music)
    print(user_get_music.json())
    response = httpx.post("http://127.0.0.1:8000/music/get_music", json=user_get_music.dict(), timeout=None)
    path = response.headers["user_music_path"] + response.headers["id"] + ".wav"
    with open(path, "wb") as file:
        for chunk in response.iter_bytes():
            file.write(chunk)

    return {"path": path}


def get_music_by_id(music_id: str, user_id: str):
    music_info = MusicInfo(music_id=music_id, user_id=user_id)
    response = httpx.post("http://127.0.0.1:8000/music/get_music_by_id", json=music_info.dict(), timeout=None)
    path = response.headers["user_music_path"] + response.headers["id"] + ".wav"
    with open(path, "wb") as file:
        for chunk in response.iter_bytes():
            file.write(chunk)

    return {"path": path}
