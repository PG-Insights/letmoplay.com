#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 12:56:04 2023

@author: dale
"""

from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from db.session import get_db
from db.repository.blogs import get_all_blogs_data_dict


router = APIRouter()

@router.get("/", response_model=None)
async def get_blogs_db_table_dict(db: Session = Depends(get_db)):
    return get_all_blogs_data_dict(db=db)

