#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 10:35:12 2023

@author: dale
"""

from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from route_general_pages import templates
from get_all_blogs_dict import get_all_blogs_dict
from pathlib import Path

async def get_all_blogs_for_error_nav():
    blog_file_path = Path(
        Path(__file__).parents[3],
        'templates',
        'general_pages', 
        'blogs',
    )
    return get_all_blogs_dict(blog_file_path)

async def not_found_exception_handler(request: Request, exc: StarletteHTTPException):
    blogs_dict = await get_all_blogs_for_error_nav()
    return templates.TemplateResponse(
        "general_pages/404.html", 
        {
            "request": request,
            "all_blogs_dict": blogs_dict,
        },
        status_code=404
    )