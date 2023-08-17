#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 22:03:02 2023

@author: dale
"""

from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from db.session import get_db
from schemas.simple_messages import SimpleMessageCreate
from db.repository.simple_messages import create_new_simple_message

router = APIRouter()

@router.post("/", response_model=None)
def create_simple_message(
    simple_message: SimpleMessageCreate,
    db: Session = Depends(get_db)
):
    simple_message = create_new_simple_message(
        simple_message=simple_message,
        db=db
    )
    return simple_message