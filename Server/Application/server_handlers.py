from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
from Server.Application.__init__ import get_server_application
from Server.Application.__init__ import get_users_repository

router = APIRouter()
users_rep = get_users_repository()


class MusicTransfer(BaseModel):
    id: int
    name: str
    date: datetime
    file: bytes


class UserInformation(BaseModel):
    login: str
    password: str


class UserGetMusic(BaseModel):
    user_id: int
    style_music: list
    music_length: int = 5  # ["angry","dark"]


# {"Angry": True, "Romantic": False, "Happy": False, "Sad": True, "Dark": True, "Dreamy": False, "Sentimental": False, "Mysterious": False}

@router.post('/get_music', response_model=MusicTransfer)
async def get_music(user_get_music: UserGetMusic):
    music_item = get_server_application().generate_music_by_phrase(None, user_get_music.style_music,
                                                                   user_get_music.music_length)
    file_path = music_item.path + music_item.id + ".wav"
    while not music_item.is_ready:
        pass
    print("has been generated")
    user_music_item = music_item.copy().change_path("../Application/GettingExamples/")  # добавить path
    return FileResponse(file_path, filename=user_music_item.id, headers={"id": f"{user_music_item.id}",
                                                                         "user_music_path": f"{user_music_item.path}",
                                                                         "music_length": f"{user_music_item.length_in_seconds}",
                                                                         })


@router.post('/auth/sign-up')
async def sign_up(user_information: UserInformation):
    user = users_rep.register_user(user_information.login, user_information.password)
    if not user:
        return {"message": "The user has already been created"}
    return {"message": "The user has been successfully created", "id": user.user_id}


@router.post('/auth/sign-in')
async def sign_in(user_information: UserInformation):
    user = users_rep.get_user_by_login_and_password(user_information.login,
                                                    user_information.password)
    if not user:
        return {"message": "Login or password is incorrect"}
    return {"message": "Successfully logged in", "id": user.user_id}
