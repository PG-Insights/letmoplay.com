#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Sun Mar  5 21:17:34 2023

@author: dale
'''
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME:str = 'Let MO Play'
    PROJECT_VERSION: str = '1.0.1'
    
    POSTGRES_USER : str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SERVER : str = os.getenv('POSTGRES_SERVER')
    POSTGRES_PORT : str = os.getenv('POSTGRES_PORT')
    POSTGRES_DB : str = os.getenv('POSTGRES_DB')
    DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'

settings = Settings()
