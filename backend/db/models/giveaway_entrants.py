# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Boolean, Date

from db.base_class import Base


class Entrant(Base):
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    name = Column(
        String,
        nullable=True,
        default='None'
    )
    email = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )
    zip_code = Column(
        String,
        nullable=True,
        default='None'
    )
    agree_tos = Column(
        Boolean(),
        default=True
    )
    date_posted = Column(
        Date
    )