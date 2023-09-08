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
    PROJECT_VERSION: str = '1.2.0'

    SUPABASE_ID : str = os.getenv('SUPABASE_ID')
    SUPA_PORT = os.getenv('SUPA_PORT')
    SUPABASE_URL : str = os.getenv('SUPABASE_URL')
    SUPA_PUBLIC_KEY : str = os.getenv('SUPA_PUBLIC_KEY')
    SUPA_PRIVATE_KEY : str = os.getenv('SUPA_PRIVATE_KEY')
    SUPA_PASSWORD = os.getenv('SUPA_PASSWORD')
    JWT_SECRET : str = os.getenv('JWT_SECRET')
    PERSONAL_ACCESS : str = os.getenv('PERSONAL_ACCESS')
    LMP_BUCKET : str = os.getenv('LMP_BUCKET')
    SUPA_URL: str = f'postgresql://postgres:{SUPA_PASSWORD}@db.{SUPABASE_ID}.supabase.co:{SUPA_PORT}/postgres'
    
settings = Settings()
