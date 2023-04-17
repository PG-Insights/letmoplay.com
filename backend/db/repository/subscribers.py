#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 20:06:47 2023

@author: dale
"""

from sqlalchemy.orm import Session
from schemas.subscribers import SubscriberCreate
from db.models.subscribers import Subscriber
from datetime import datetime


def create_new_subscriber(
        subscriber:SubscriberCreate,
        db:Session):
    subscriber = Subscriber(
        email = subscriber.email,
        agree_tos=True,
        date_posted=datetime.now()
    )
    db.add(subscriber)
    db.commit()
    db.refresh(subscriber)
    
    return subscriber
