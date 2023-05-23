# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Boolean, Date

from db.base_class import Base


class Entrant(Base):
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