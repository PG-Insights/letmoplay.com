#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 21:13:37 2023

@author: dale
"""

from sqlalchemy.orm import Session
from schemas.users import UserCreate
from db.models.users import Lmp_User as User
from datetime import date
#from core.hashing import Hasher

def create_new_user(user:UserCreate,db:Session):
    user = User(
        username=user.username,
        email = user.email,
        password=user.password,
        zip_code=user.zip_code,
        is_active=True,
        is_superuser=False,
        date_posted=date.today()
    )
    try:
        db.add(user)
    except:
        db.rollback()
    else:
        db.commit()
        db.refresh(user)
    finally:
        return user
