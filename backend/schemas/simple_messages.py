# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field, EmailStr, constr
from datetime import datetime
from typing import Optional

class SimpleMessageCreate(BaseModel):
    name: Optional[constr(max_length=149)] = ''
    email: EmailStr
    message: Optional[constr(max_length=999)] = ''
    date_posted: datetime = Field(default_factory=datetime.now)
