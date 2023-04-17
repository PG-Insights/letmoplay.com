#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 21:12:40 2023

@author: dale
"""

from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends

from schemas.subscribers import SubscriberCreate, ShowSubscriber
from db.session import get_db
from db.repository.subscribers import create_new_subscriber

router = APIRouter()


@router.post("/", response_model=ShowSubscriber)
def create_subscriber(
    subscriber: SubscriberCreate,
    db: Session = Depends(get_db)
):
    subscriber = create_new_subscriber(
        subscriber=subscriber,
        db=db
    )
    return subscriber
