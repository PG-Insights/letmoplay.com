# -*- coding: utf-8 -*-

import uuid
from sqlalchemy import Column, String, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID
from db.base_class import Base
from datetime import date

class Lmp_Entrant(Base):
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
    zip_code = Column(
        String,
        nullable=True,
        default=None,
    )
    date_posted = Column(
        Date,
        default=date.today()
    )