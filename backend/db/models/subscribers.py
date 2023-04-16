#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 20:02:12 2023

@author: dale
"""

from sqlalchemy import Column, Integer, String, Boolean, Date

from db.base_class import Base


class Subscriber(Base):
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    email = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )
    agree_tos = Column(
        Boolean(),
        default=True
    )
    date_posted = Column(
        Date
    )