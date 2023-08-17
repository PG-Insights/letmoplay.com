#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 21:56:33 2023

@author: dale
"""

from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from db.base_class import Base


class Lmp_SimpleMessage(Base):
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    name = Column(
        String,
        default='None'
    )
    email = Column(
        String,
        nullable=False,
    )
    message = Column(
        String,
        nullable=True,
    )
    date_posted = Column(
        Date,
        default=datetime.now()
    )