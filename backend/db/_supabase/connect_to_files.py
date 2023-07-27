#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 16:55:56 2023

@author: dale
"""

from db._supabase import supa_client


async def get_storage_result_list() -> list[dict]:    
    bucket = await supa_client.get_lmp_bucket()
    return bucket.list(path='/')
       

async def get_image_from_results(file_name: str):
    file_path=f"images/{file_name}"
    bucket = supa_client.get_lmp_bucket()
    return bucket.download(
        path=file_path
    )
        