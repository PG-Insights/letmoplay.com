# -*- coding: utf-8 -*-

from pydantic import BaseModel, EmailStr


class EntrantCreate(BaseModel):
    name: str
    email : EmailStr
    zip_code: str
    agree_tos: bool
    

class ShowEntrant(BaseModel):
    email : EmailStr

    class Config():
        orm_mode = True