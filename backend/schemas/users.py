#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 20:51:36 2023

@author: dale
"""

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    zip_code: str = None


class ShowUser(BaseModel):
    username: str
    email: EmailStr
    is_active: str

    class Config():
        orm_mode = True
