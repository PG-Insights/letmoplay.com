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
from db.models.subscribers import Subscriber

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


def remove_subscriber(subscriber_email: str,
                      db: Session = Depends(get_db)
                      ):
    # Query the database to find the subscriber with the given email
    subscriber = db.query(Subscriber).filter(Subscriber.email == subscriber_email).first()

    # If the subscriber is found, delete the record and commit the changes
    if subscriber:
        db.delete(subscriber)
        db.commit()
        return {"email": subscriber_email}