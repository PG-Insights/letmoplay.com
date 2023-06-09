#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 21:13:44 2023

@author: dale
"""

import sys
from pathlib import Path

MAIN_DIR = Path(__file__).parent
BACKEND_DIR = Path(MAIN_DIR, 'backend')
API_DIR = Path(BACKEND_DIR, 'apis')
VERSION1_DIR = Path(API_DIR, 'version1')
CORE_DIR = Path(BACKEND_DIR, 'core')
TEMPLATES_DIR = Path(BACKEND_DIR, 'templates')
STATIC_DIR = Path(BACKEND_DIR, 'static')
DB_DIR = Path(BACKEND_DIR, 'db')
MODELS_DIR = Path(DB_DIR, 'models')


if str(MAIN_DIR) not in sys.path:
    sys.path.append(str(MAIN_DIR))
    
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))
    
if str(API_DIR) not in sys.path:
    sys.path.append(str(API_DIR))
    
if str(VERSION1_DIR) not in sys.path:
    sys.path.append(str(VERSION1_DIR))
    
if str(CORE_DIR) not in sys.path:   
    sys.path.append(str(CORE_DIR))
    
if str(TEMPLATES_DIR) not in sys.path:
    sys.path.append(str(TEMPLATES_DIR))
    
if str(STATIC_DIR) not in sys.path:
    sys.path.append(str(STATIC_DIR))
    
if str(MODELS_DIR) not in sys.path: 
    sys.path.append(str(MODELS_DIR))
    

from fastapi import FastAPI, status
from core.config import settings
from apis.base import api_router
from middleware.custom_error_middleware import not_found_exception_handler
from fastapi.staticfiles import StaticFiles
from db.session import engine
from db.base import Base


def include_router(app):
    app.include_router(api_router)
    

def include_customer_404_handler(app):
    app.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found_exception_handler)
    

def configure_static(app):
    global STATIC_DIR
    app.mount(
        str(STATIC_DIR), 
        StaticFiles(directory=str(STATIC_DIR)),
        name="static"
    )
    

def create_tables():
    print("create_tables")
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    include_customer_404_handler(app)
    include_router(app)
    configure_static(app)
    create_tables()
    return app 


app = start_application()
    