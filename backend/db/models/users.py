#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 19:17:04 2023

@author: dale
"""

import uuid
from sqlalchemy import Column, String, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID
from db.base_class import Base
from datetime import date

class Lmp_User(Base):
    id = Column(
        UUID,
        primary_key=True,
        index=True,
        default=uuid.uuid4
    )
    username = Column(
        String,
        unique=True,
        nullable=False
    )
    email = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )
    password = Column(
        String,
        nullable=False
    )
    zip_code = Column(
        String,
        nullable=True,
        default=None
    )
    date_posted = Column(
        Date,
        default=date.today()
    )
    is_active = Column(
        Boolean(),
        default=True
    )
    is_superuser = Column(
        Boolean(),
        default=False
    )
    