#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 21:53:12 2023

@author: dale
"""

from sqlalchemy.orm import Session
from schemas.simple_messages import SimpleMessageCreate
from db.models.simple_messages import Lmp_SimpleMessage


def create_new_simple_message(
        simple_message: SimpleMessageCreate,
        db: Session):
    created_message = Lmp_SimpleMessage(
        name=simple_message.name,
        email=simple_message.email,
        message=simple_message.message,
    )
    try:
        db.add(created_message)
    except:
        print('\nMessage to Db addition failed\n')
        db.rollback()
    else:
        db.commit()
        db.refresh(created_message)

    return created_message
