#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 20:06:47 2023

@author: dale
"""

from sqlalchemy.orm import Session
from psycopg2.errors import UniqueViolation
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
    try:
        db.add(subscriber)
    except UniqueViolation:
        db.rollback()
    else:
        db.commit()
        db.refresh(subscriber)
    finally:
        return subscriber


def remove_subscriber(
        subscriber_email: str,
        db:Session):
    subscriber = db.query(
        Subscriber
    ).filter(Subscriber.email == subscriber_email).first()

    if subscriber:
        db.delete(subscriber)
        db.commit()
        return {"email": subscriber_email}