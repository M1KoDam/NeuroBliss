from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from Server.Application.__init__ import get_server_application
from Server.Application.__init__ import get_users_repository, get_music_repository

router = APIRouter()
users_rep = get_users_repository()
music_rep = get_music_repository()
global condition
condition = True


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
    style_music: str  # "angry"
    music_length: int


class MusicInfo(BaseModel):
    music_id: str
    user_id: str


@router.post('/music/get_music')
async def get_music(user_get_music: UserGetMusic):
    music_item = get_server_application().generate_music_by_phrase(user_get_music.style_music,
                                                                   user_get_music.music_length)
    file_path = music_item.path + music_item.id + ".wav"
    while not music_item.is_ready:
        pass
    return FileResponse(file_path, filename=music_item.id, headers={"id": f"{music_item.id}",
                                                                    "music_length": f"{music_item.length_in_seconds}"
                                                                    })


@router.post('/music/download_music_by_id')
async def download_music_by_id(music_info: MusicInfo):
    music_item = music_rep.get_music_by_id(music_info.music_id)
    if music_item is None:
        message = {"message": False}
        headers = {"message": "False"}
        return JSONResponse(message, headers=headers, status_code=404)

    file_path = music_item.path + music_item.id + ".wav"
    return FileResponse(file_path, filename=music_item.id, headers={"id": f"{music_item.id}",
                                                                    "music_length": f"{music_item.length_in_seconds}"
                                                                    }, status_code=200)


@router.post('/music/get_music_by_id')
async def get_music_by_id(music_info: MusicInfo):
    temp1 = "ece5415a-46b4-4dcf-9f86-6befebfdcf5c"
    temp2 = "9c66043b-b06b-481f-822e-fdd1272523dc"
    global condition

    if condition:
        condition = False
        selected_option = temp1

    else:
        selected_option = temp2
        condition = True
    print(selected_option)
    music_item = music_rep.get_music_by_id(selected_option)
    if music_item is None:
        message = {"message": False}
        return JSONResponse(message, status_code=404)

    file_path = music_item.path + music_item.id + ".wav"
    return FileResponse(file_path, filename=music_item.id, headers={"message": True,
                                                                    "id": f"{music_item.id}",
                                                                    "music_length": f"{music_item.length_in_seconds}"
                                                                    }, status_code=200)


@router.post('/auth/sign-up')
async def sign_up(user_information: UserInformation):
    user = users_rep.register_user(user_information.login, user_information.password)
    if not user:
        return {"message": False}
    return {"message": True, "id": user.user_id}


@router.post('/auth/sign-in')
async def sign_in(user_information: UserInformation):
    user = users_rep.get_user_by_login_and_password(user_information.login,
                                                    user_information.password)
    if not user:
        return {"message": False}
    return {"message": True, "id": user.user_id, "user_liked": user.liked}


@router.post('/auth/del_user')
async def delete_user(user_information: UserInformation):
    return {"message": "The user was successfully deleted"}


@router.post('/music/add_music_to_liked')
async def add_to_liked(music_info: MusicInfo):
    trying_add = users_rep.get_user_by_id(music_info.user_id).add_music_to_liked(music_info.music_id)
    if trying_add:
        users_rep.update_json()
        return {"message": True}
    else:
        return {"message": False}


@router.post('/music/delete_music_from_liked')
async def delete_from_liked(music_info: MusicInfo):
    trying_delete = users_rep.get_user_by_id(music_info.user_id).delete_music_from_liked(music_info.music_id)

    if trying_delete:
        users_rep.update_json()
        return {"message": True}
    else:
        return {"message": False}
