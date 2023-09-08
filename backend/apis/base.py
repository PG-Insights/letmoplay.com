#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 21:36:01 2023

@author: dale
"""

from fastapi import APIRouter
import route_general_pages
import route_subscribers
import route_giveaway_entrants
import route_simple_messages

api_router = APIRouter()
api_router.include_router(
    route_general_pages.general_pages_router,
    prefix="",
    tags=["general_pages"]
)
api_router.include_router(
    route_subscribers.router,
    prefix="/subscribers",
    tags=["subscriber"]
)
api_router.include_router(
    route_giveaway_entrants.router,
    prefix="/entrants",
    tags=["entrant"]
)
api_router.include_router(
    route_simple_messages.router,
    prefix="/messages",
    tags=["message"]
)