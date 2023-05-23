# -*- coding: utf-8 -*-

from pydantic import BaseModel, EmailStr


class EntrantCreate(BaseModel):
    email : EmailStr
    

class ShowEntrant(BaseModel):
    email : EmailStr

    class Config():
        orm_mode = True