#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 20:02:12 2023

@author: dale
"""

import uuid
from sqlalchemy import Column, String, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID
from db.base_class import Base
from datetime import date


class Lmp_Subscriber(Base):
    id = Column(
        UUID,
        primary_key=True,
        index=True,
        default=uuid.uuid4
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
        Date,
        default=date.today()
    )