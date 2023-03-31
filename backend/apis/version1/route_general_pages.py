#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 21:10:59 2023

@author: dale
"""

import os
import pandas as pd
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates_dir = Path(
    Path(__file__).parents[2],
    'templates',
)

templates = Jinja2Templates(directory=str(templates_dir))
general_pages_router = APIRouter()


@general_pages_router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'homepage.html'
            )
        ),
        {
            "request": request,
        },
    )


@general_pages_router.get("/form", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse(
        str(
            Path(
                'components',
                'form.html'
            )
        ),
        {
            "request": request
        }
    )


@general_pages_router.post("/submit", response_model=None)
async def submit_form(request: Request,
                      name: str = Form(...),
                      email: str = Form(...),
                      subject: str = Form(...),
                      message: str = Form(...)
                      ) -> templates.TemplateResponse:
    # Create DataFrame
    data = {
        'Name': [str(name)],
        'Email': [str(email)],
        'Subject': [str(subject)],
        'Message': [str(message)],
        'Timestamp': [str(datetime.now())]
    }
    df = pd.DataFrame(data)
    data_path = Path(
        '.',
        'backend',
        'db',
        'emails_db',
        'subscribers.csv'
    )
    if os.path.exists(str(data_path)):
        df = pd.concat(
            [
                pd.read_csv(str(data_path)).copy(),
                df.copy()
            ],
            axis=0
        )
    # Save to CSV file
    df.to_csv(str(data_path), index=False)

    # Render success template
    return templates.TemplateResponse(
        str(
            Path(
                'components',
                'success.html'
            )
        ),
        {
            "request": request,
            "name": name,
        }
    )


@general_pages_router.get("/email-form", response_class=HTMLResponse)
async def email_form(request: Request):
    return templates.TemplateResponse(
        str(
            Path(
                'components',
                'email-form.html'
            )
        ),
        {
            "request": request
        }
    )


@general_pages_router.post("/submit-email", response_model=None)
async def submit_email_form(request: Request,
                            email: str = Form(...),
                            ) -> templates.TemplateResponse:
    # Create DataFrame
    data = {
        'Name': ['None'],
        'Email': [str(email)],
        'Subject': ['None'],
        'Message': ['None'],
        'Timestamp': [str(datetime.now())]
    }
    df = pd.DataFrame(data)
    data_path = Path(
        '.',
        'backend',
        'db',
        'emails_db',
        'subscribers.csv'
    )
    if os.path.exists(str(data_path)):
        df = pd.concat(
            [
                pd.read_csv(str(data_path)).copy(),
                df.copy()
            ],
            axis=0
        )
    # Save to CSV file
    df.to_csv(str(data_path), index=False)

    # Render success template
    return templates.TemplateResponse(
        str(
            Path(
                'components',
                'success.html'
            )
        ),
        {
            "request": request,
            "name": email,
        }
    )


@general_pages_router.get("/unsubscribe", response_class=HTMLResponse)
async def unsubscribe(
    request: Request
):

    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'unsubscribe.html'
            )
        ),
        {
            "request": request,
        },
    )


@general_pages_router.post("/unsubscribe-submit", response_model=None)
async def submit_unsubscribe_form(
    request: Request,
    email: str = Form(...),
) -> templates.TemplateResponse:
    data_path = Path(
        '.',
        'backend',
        'db',
        'emails_db',
        'subscribers.csv'
    )
    if os.path.exists(str(data_path)):
        df = pd.read_csv(str(data_path))
        new_df = df.copy()[
            df['Email'].str.casefold() != (str(email).casefold())
        ]
        new_df.to_csv(str(data_path), index=False)
    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'homepage.html'
            )
        ),
        {
            "request": request,
        },
    )
