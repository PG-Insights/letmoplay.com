#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 10:35:12 2023

@author: dale
"""

from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from route_general_pages import templates

async def not_found_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse(
        "general_pages/404.html", 
        {
            "request": request
        },
        status_code=404
    )