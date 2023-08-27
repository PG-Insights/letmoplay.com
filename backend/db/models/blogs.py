#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 12:41:13 2023

@author: dale
"""

from sqlalchemy import Column, Integer, String, Date, ARRAY
from datetime import datetime
from db.base_class import Base


class Lmp_Blogs(Base):
    table_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    title = Column(
        String,
        nullable=True,
    )
    creative_path = Column(
        String,
        nullable=True,
    )
    creative_alt = Column(
        String,
        nullable=True,
    )
    blog_link = Column(
        String,
        nullable=True,
    )
    blog_description = Column(
        String,
        nullable=True,
    )
    portfolio_groups = Column(
        ARRAY(String),
        default=['filter-bets', 'filter-law', 'filter-sports']
    )
    upload_date = Column(
        Date,
        default=datetime.now()
    )