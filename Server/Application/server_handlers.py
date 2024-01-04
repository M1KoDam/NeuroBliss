from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class MusicTransfer(BaseModel):
    id: int
    name: str
    date: datetime
    file: bytes


class UserInformation(BaseModel):
    email: str
    password: str


class UserGetMusic(BaseModel):
    UserId: int
    styleMusic: list  # ["angry","dark"]


@router.post('/authorization', name='user:login')
def authorization(user: UserInformation):
    return {'status': 'OK'}


# {"Angry": True, "Romantic": False, "Happy": False, "Sad": True, "Dark": True, "Dreamy": False, "Sentimental": False, "Mysterious": False}

@router.get('/get_music', response_model=MusicTransfer)
def get_music(user_get_music: UserGetMusic):
    return {'status': 'OK'}

