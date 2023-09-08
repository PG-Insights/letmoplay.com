#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 12:47:06 2023

@author: dale
"""

import base64
from sqlalchemy.orm import Session
from db.models.blogs import Lmp_Blogs as Blogs


def get_last_9_entries_from_dict(original_dict):
    last_9_keys = list(original_dict.keys())[-9:]
    return {k: original_dict[k] for k in last_9_keys}


def get_all_blogs_data_dict(db: Session):
    all_content_data = db.query(Blogs).all()
    result_dict = {
        row.table_id: {
            column.name: getattr(row, column.name) for column in
            Blogs.__table__.columns if column.name != 'table_id'
        }
        for row in all_content_data
    }
    return get_last_9_entries_from_dict(result_dict)
    
    
def convert_img_bytes_for_html(img_bytes):
    return base64.b64encode(img_bytes).decode()