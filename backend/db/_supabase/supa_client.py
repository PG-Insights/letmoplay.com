# -*- coding: utf-8 -*-

from core.config import settings
from supabase import create_client, Client


async def return_created_client(
        url: str = settings.SUPABASE_URL,
        key: str = settings.SUPA_PRIVATE_KEY) -> Client:
    return create_client(url, key)


async def get_storage_bucket():    
    client = await return_created_client()
    return client.storage.get_bucket(
        settings.STORAGE_BUCKET, 
    ) 