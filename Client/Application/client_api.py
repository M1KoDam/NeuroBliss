from pydantic import BaseModel
import httpx
from hashlib import sha256
from os import getcwd
from pathlib import Path
import os

server = "127.0.0.1:8000"
MUSIC_CACHE_PATH = "../Application/Cache/"
MUSIC_DATA_PATH = "../Application/Data/"
CURRENT_DIR = os.getcwd()
global Is_InApp
Is_InApp = False


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
    if user_id is None or style_music is None:
        return {"status": False, "path": None, "music_id": None}
    user_get_music = UserGetMusic(user_id=user_id, style_music=style_music)
    return _connection_to_server_get_music(user_get_music,
                                           f"http://{server}/music/get_music",
                                           path_to_save=MUSIC_CACHE_PATH, is_cached=True)


def get_music_by_id(music_id: str, user_id: str):
    if music_id is None or user_id is None:
        return {"status": False, "path": None, "music_id": None}
    music_info = MusicInfo(music_id=music_id, user_id=user_id)
    return _connection_to_server_get_music(music_info,
                                           f"http://{server}/music/get_music_by_id",
                                           path_to_save=MUSIC_CACHE_PATH, is_cached=True)


def download_music_by_id(music_id: str, user_id: str):
    if music_id is None or user_id is None:
        return {"status": False, "path": None, "music_id": None}
    music_info = MusicInfo(music_id=music_id, user_id=user_id)
    return _connection_to_server_get_music(music_info,
                                           f"http://{server}/music/download_music_by_id",
                                           path_to_save=MUSIC_DATA_PATH, is_cached=False)


def _connection_to_server_get_music(music_info, server_str: str, path_to_save: str, is_cached: bool):
    try:
        response = httpx.post(server_str, json=music_info.dict(), timeout=None)
        path = path_to_save + response.headers["id"] + ".wav"
        full_path = get_path_to_user_info('Cache' if is_cached else 'Data', response.headers["id"]+".wav")
        if not os.path.exists(full_path):
            with open(full_path, "wb") as file:
                for chunk in response.iter_bytes():
                    file.write(chunk)

        return {"status": True, "path": full_path, "music_id": response.headers["id"]}
    except httpx.ConnectError:
        return {"status": False, "path": None, "music_id": None}


def add_to_liked(music_id: str, user_id: str):
    json = {"music_id": music_id, "user_id": user_id}
    response = httpx.post(f"http://{server}/music/add_music_to_liked", json=json, timeout=None)
    return response.json()  # {"message": True/False}, true - added


def delete_from_liked(music_id: str, user_id: str):
    json = {"music_id": music_id, "user_id": user_id}
    response = httpx.post(f"http://{server}/music/delete_music_from_liked", json=json, timeout=None)
    return response.json()  # {"message": True/False}, true - deleted


def get_path_to_user_info(cached_or_data, music_id) -> Path:
    global Is_InApp
    if not Is_InApp:
        parent_dir = os.path.dirname(CURRENT_DIR)
        os.chdir(parent_dir)
        Is_InApp = True
    path = str(
        Path(str(getcwd())) / 'Application' / cached_or_data / music_id
    )
    return Path(path)
