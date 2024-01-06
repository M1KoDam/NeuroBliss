from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
from Server.Application.__init__ import get_server_application
from Server.Application.__init__ import get_users_repository, get_music_repository

router = APIRouter()
users_rep = get_users_repository()
music_rep = get_music_repository()


class MusicTransfer(BaseModel):
    id: int
    name: str
    date: datetime
    file: bytes


class UserInformation(BaseModel):
    login: str
    password: str
    user_id: str | None


class UserGetMusic(BaseModel):
    user_id: str
    style_music: list
    music_length: int  # ["angry","dark"]


class MusicInfo(BaseModel):
    music_id: str
    user_id: str


@router.post('/music/get_music')
async def get_music(user_get_music: UserGetMusic):
    music_item = get_server_application().generate_music_by_phrase(None, user_get_music.style_music,
                                                                   user_get_music.music_length)
    file_path = music_item.path + music_item.id + ".wav"
    while not music_item.is_ready:
        pass
    print("has been generated")
    user_music_item = music_item.copy().change_path("Client/Application/Cache/")  # добавить path
    return FileResponse(file_path, filename=user_music_item.id, headers={"id": f"{user_music_item.id}",
                                                                         "user_music_path": f"{user_music_item.path}",
                                                                         "music_length": f"{user_music_item.length_in_seconds}",
                                                                         })


@router.post('/music/download_music_by_id')
async def download_music_by_id(music_info: MusicInfo):
    music_item = music_rep.get_music_by_id(music_info.music_id)
    file_path = music_item.path + music_item.id + ".wav"
    user_music_item = music_item.copy().change_path("Client/Application/Data/")

    return FileResponse(file_path, filename=user_music_item.id, headers={"id": f"{user_music_item.id}",
                                                                         "user_music_path": f"{user_music_item.path}",
                                                                         "music_length": f"{user_music_item.length_in_seconds}",
                                                                         })


@router.post('/music/get_music_by_id')
async def get_music_by_id(music_info: MusicInfo):
    music_item = music_rep.get_music_by_id(music_info.music_id)
    file_path = music_item.path + music_item.id + ".wav"
    user_music_item = music_item.copy().change_path("Client/Application/Cache/")

    return FileResponse(file_path, filename=user_music_item.id, headers={"id": f"{user_music_item.id}",
                                                                         "user_music_path": f"{user_music_item.path}",
                                                                         "music_length": f"{user_music_item.length_in_seconds}",
                                                                         })


@router.post('/auth/sign-up')
async def sign_up(user_information: UserInformation):
    user = users_rep.register_user(user_information.login, user_information.password)
    if not user:
        return {"message": False}
    return {"message": True, "id": "user.user_id"}


@router.post('/auth/sign-in')
async def sign_in(user_information: UserInformation):
    user = users_rep.get_user_by_login_and_password(user_information.login,
                                                    user_information.password)
    if not user:
        return {"message": "Login or password is incorrect"}
    return {"message": "Successfully logged in", "id": user.user_id}


@router.post('/auth/del_user')
async def delete_user(user_information: UserInformation):
    return {"message": "The user was successfully deleted"}


@router.post('/music/add_music_to_playlist')
async def add_playlist(music_info: MusicInfo):
    users_rep.get_user_by_id(music_info.user_id).add_music_to_liked(music_info.music_id)
    users_rep.update_json()
    return {"message": True}
