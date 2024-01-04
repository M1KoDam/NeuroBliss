from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime
from Server.Domain.user import User
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
    UserId: int
    styleMusic: list  # ["angry","dark"]


# {"Angry": True, "Romantic": False, "Happy": False, "Sad": True, "Dark": True, "Dreamy": False, "Sentimental": False, "Mysterious": False}

@router.post('/get_music', response_model=MusicTransfer)
def get_music(user_get_music: UserGetMusic):
    name = user_get_music.UserId
    return {'status': 'OK'}


@router.post('/auth/sign-up')
def sign_up(user_information: UserInformation):
    user = users_rep.register_user(user_information.login, user_information.password)
    if not user:
        return {"message": "The user has already been created"}
    return {"message": "The user has been successfully created", "id": user.user_id}


@router.post('/auth/sign-in')
def sign_in(user_information: UserInformation):
    user = users_rep.get_user_by_login_and_password(user_information.login,
                                                                       user_information.password)
    if not user:
        return {"message": "Login or password is incorrect"}
    return {"message": "Successfully logged in", "id": user.user_id}
