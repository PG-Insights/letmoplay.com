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
from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from get_all_blogs_dict import get_all_blogs_dict
from route_subscribers import create_subscriber, remove_subscriber
from schemas.subscribers import SubscriberCreate
from db.session import get_db

templates_dir = Path(
    Path(__file__).parents[2],
    'templates',
)

templates = Jinja2Templates(directory=str(templates_dir))
general_pages_router = APIRouter()


async def get_all_blogs_for_nav():
    blog_file_path = Path(
        Path(__file__).parents[2],
        'templates',
        'general_pages', 
        'blogs',
    )
    return get_all_blogs_dict(blog_file_path)


@general_pages_router.get("/")
async def home(request: Request):
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'homepage.html'
            )
        ),
        {
            "request": request,
            "all_blogs_dict": blogs_dict,
        },
    )

@general_pages_router.get("/privacy-policy")
async def privacy_policy(request: Request):
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'privacy-policy.html'
            )
        ),
        {
            "request": request,
            "all_blogs_dict": blogs_dict,
        },
    )

@general_pages_router.get("/user-agreement")
async def terms_of_use(request: Request):
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'user-agreement.html'
            )
        ),
        {
            "request": request,
            "all_blogs_dict": blogs_dict,
        },
    )


@general_pages_router.get("/blogs")
async def blogs(request: Request):
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'blogs.html'
            )
        ),
        {
            "request": request,
            "all_blogs_dict": blogs_dict,
        },
    )

@general_pages_router.get("/sponsors/sign-up/tiers")
async def sponsors_info_page(request: Request):
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'sponsors',
                'sign-up',
                'tiers.html'
            )
        ),
        {
            "request": request,
            "all_blogs_dict": blogs_dict,
        },
    )


@general_pages_router.get("/join-the-cause")
async def join_the_cause_landing(request: Request):
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'join-the-cause.html'
            )
        ),
        {
            "request": request,
            "all_blogs_dict": blogs_dict,
        },
    )


@general_pages_router.get("/stlsc-tickets-giveaway")
async def stlsc_giveaway(request: Request):
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'join-the-cause.html'
            )
        ),
        {
            "request": request,
            "all_blogs_dict": blogs_dict,
        },
    )


@general_pages_router.get("/derby-giveaway-with-macs-downtown")
async def macs_derby_giveaway(request: Request):
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'join-the-cause.html'
            )
        ),
        {
            "request": request,
            "all_blogs_dict": blogs_dict,
        },
    )


@general_pages_router.get("/contact")
async def contact(request: Request):
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'contact.html'
            )
        ),
        {
            "request": request,
            "all_blogs_dict": blogs_dict,
        },
    )


@general_pages_router.get("/blogs/{blog_name:path}")
async def blog(
    request: Request,
    blog_name: str,
):
    # Construct the path to the blog file
    blog_file_path = Path(
        Path(__file__).parents[2],
        'templates',
        'general_pages', 
        'blogs',
        f'{blog_name}.html',
    )

    if not blog_file_path.is_file():
        raise HTTPException(
            status_code=404, 
            detail="Blog file not found"
        )
    template_path = Path(
        'general_pages',
        'blogs',
        f'{blog_name}.html',
    )
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(template_path),
        {
            "request": request,
            "all_blogs_dict": blogs_dict,
        },
    )

@general_pages_router.get("/form", response_class=HTMLResponse)
async def form(request: Request):
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(
            Path(
                'components',
                'form.html'
            )
        ),
        {
            "request": request,
            "all_blogs_dict": blogs_dict,
            
        }
    )


@general_pages_router.post("/submit", response_model=None)
async def submit_form(request: Request,
                      name: str = Form(...),
                      email: str = Form(...),
                      subject: str = Form(...),
                      message: str = Form(...),
                      db: Session = Depends(get_db),
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
        
    # Drop duplicates
    df = df.copy().drop_duplicates(
        subset=[
            'Email', 
            'Message',
        ],
        ignore_index=True,
    )
    
    # Save to CSV file
    df.to_csv(str(data_path), index=False)
    
    subscriber_data = SubscriberCreate(email=email)
    create_subscriber(subscriber=subscriber_data, db=db)

    # Render success template
    blogs_dict = await get_all_blogs_for_nav()
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
            "all_blogs_dict": blogs_dict,
        }
    )


@general_pages_router.get("/email-form", response_class=HTMLResponse)
async def email_form(request: Request):
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(
            Path(
                'components',
                'email-form.html'
            )
        ),
        {
            "request": request,
            "all_blogs_dict": blogs_dict,
        }
    )


@general_pages_router.post("/submit-email", response_model=None)
async def submit_email_form(request: Request,
                            email: str = Form(...),
                            db: Session = Depends(get_db),
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
        
    # Drop duplicates
    df = df.copy().drop_duplicates(
        subset=[
            'Email', 
            'Message',
        ],
        ignore_index=True,
    )
    
    # Save to CSV file
    df.to_csv(str(data_path), index=False)

    # Render success template
    blogs_dict = await get_all_blogs_for_nav()

    subscriber_data = SubscriberCreate(email=email)
    create_subscriber(subscriber=subscriber_data, db=db)
    
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
            "all_blogs_dict": blogs_dict,
        }
    )


@general_pages_router.get("/unsubscribe", response_class=HTMLResponse)
async def unsubscribe(
    request: Request
):
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'unsubscribe.html'
            )
        ),
        {
            "request": request,
            "all_blogs_dict": blogs_dict,
        },
    )


@general_pages_router.post("/unsubscribe-submit", response_model=None)
async def submit_unsubscribe_form(
    request: Request,
    email: str = Form(...),
    db: Session = Depends(get_db)
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
    remove_subscriber(email, db=db)
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'homepage.html'
            )
        ),
        {
            "request": request,
            "all_blogs_dict": blogs_dict,
        },
    )


@general_pages_router.get("/sitemap.xml")
async def sitemap(request: Request):
    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'sitemap.xml'
            )
        ),
        {
            "request": request,
        },
    )
