from pydantic import BaseModel
import httpx
from hashlib import sha256

server = "127.0.0.1:8000"


class UserInformation(BaseModel):
    login: str
    password: str
    user_id: str | None


class UserGetMusic(BaseModel):
    user_id: str
    style_music: str
    music_length: int = 5  # ["angry","dark"]


class MusicInfo(BaseModel):
    music_id: str
    user_id: str


def register_user(login: str, password: str):
    user_info = UserInformation(login=login, password=sha256(password.encode()).hexdigest(), user_id=None)
    try:
        response = httpx.post(f"http://{server}/auth/sign-up", json=user_info.dict())
        return response.json()
    except httpx.ConnectError:
        return httpx.ConnectError


def login_user(login: str, password: str):
    user_info = UserInformation(login=login, password=sha256(password.encode()).hexdigest(), user_id=None)
    try:
        response = httpx.post(f"http://{server}/auth/sign-in", json=user_info.dict())
        return response.json()
    except httpx.ConnectError:
        return httpx.ConnectError


def get_music_generation(user_id: str, style_music: str):
    user_get_music = UserGetMusic(user_id=user_id, style_music=style_music)
    return _connection_to_server_get_music(user_get_music, f"http://{server}/music/get_music")


def get_music_by_id(music_id: str, user_id: str):
    music_info = MusicInfo(music_id=music_id, user_id=user_id)
    return _connection_to_server_get_music(music_info, f"http://{server}/music/get_music_by_id")


def download_music_by_id(music_id: str, user_id: str):
    music_info = MusicInfo(music_id=music_id, user_id=user_id)
    return _connection_to_server_get_music(music_info, f"http://{server}/music/download_music_by_id")


def _connection_to_server_get_music(music_info, server_str: str):
    try:
        response = httpx.post(server_str, json=music_info.dict(), timeout=None)
        path = response.headers["user_music_path"] + response.headers["id"] + ".wav"
        with open(path, "wb") as file:
            for chunk in response.iter_bytes():
                file.write(chunk)

        return {"status": True, "path": path}
    except httpx.ConnectError:
        return {"status": "Bad connection", "path": None}


def add_to_liked(music_id: str, user_id: str):
    json = {"music_id": music_id, "user_id": user_id}
    response = httpx.post(f"http://{server}/music/add_music_to_playlist", json=json, timeout=None)
    return response.json()
