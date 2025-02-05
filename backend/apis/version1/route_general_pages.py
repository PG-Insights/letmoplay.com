#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 21:10:59 2023

@author: dale
"""


import re
from secrets import token_hex, compare_digest
from typing import Optional
from pathlib import Path
from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi import BackgroundTasks, Header
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from version1.blogs.get_all_blogs_dict import get_all_blogs_dict
from version1.blogs.route_blogs_db_table import get_blogs_db_table_dict
from db_routes.route_subscribers import create_subscriber, remove_subscriber
from db_routes.route_giveaway_entrants import create_entrant
from db_routes.route_simple_messages import create_simple_message
from schemas.subscribers import SubscriberCreate
from schemas.giveaway_entrants import EntrantCreate
from schemas.simple_messages import SimpleMessageCreate
from db.session import get_db

from version1.email.send_welcome_email import send_welcome_email
from version1.email.send_message_received_email import (
  send_message_received_email
)

templates_dir = Path(
    Path(__file__).parents[2],
    'templates',
)

templates = Jinja2Templates(directory=str(templates_dir))
general_pages_router = APIRouter()


def generate_csrf_token():
    return token_hex(16)

def constant_time_compare(val1, val2):
    return compare_digest(val1, val2)

@general_pages_router.get("/generate/")
async def generate_csrf_token_route(referer: Optional[str] = Header(None)):
    if referer and re.match(r"https?://([a-zA-Z0-9-]+\.)*letmoplay\.com/.*", referer):
        csrf_token = generate_csrf_token()
        response = JSONResponse({"csrf_token": csrf_token})
        response.set_cookie(
            "csrf_token", 
            csrf_token, 
            httponly=True, 
            secure=True,
            samesite="Strict"
        )
        return response
    else:
        raise HTTPException(status_code=403, detail="Not authorized to generate CSRF token")

@general_pages_router.post("/validate/")
async def validate_csrf_token(request: Request, csrf_token: str = Form(...)):
    cookie_csrf_token = request.cookies.get("csrf_token")
    if cookie_csrf_token is None or not constant_time_compare(csrf_token, cookie_csrf_token):
        raise HTTPException(
            status_code=403, detail="CSRF token does not match"
        )
    return {"detail": "CSRF token is valid"}


async def get_all_blogs_for_nav():
    blog_file_path = Path(
        Path(__file__).parents[2],
        'templates',
        'general_pages', 
        'blogs',
    )
    return get_all_blogs_dict(blog_file_path)


@general_pages_router.get("/")
async def home(
      request: Request,
      db: Session = Depends(get_db)
):
    blogs_dict = await get_all_blogs_for_nav()
    blogs_db_table = await get_blogs_db_table_dict(db=db)
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
            "blogs_table": blogs_db_table,
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


@general_pages_router.get("/shop")
async def shop(request: Request):
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'shop.html'
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


@general_pages_router.get("/usmnt-stl-tickets-giveaway")
async def usmnt_giveaway_landing(request: Request):
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(
            Path(
                'general_pages',
                'usmnt-stl-tickets-giveaway.html'
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


@general_pages_router.post("/submit", response_model=None)
async def submit_form(request: Request,
                      background_tasks: BackgroundTasks,
                      name: str = Form('None'),
                      email: str = Form(...),
                      subject: str = Form('None'),
                      message: str = Form('None'),
                      csrf_token: str = Form(...),
                      db: Session = Depends(get_db),
                      _: bool = Depends(validate_csrf_token),
                      ) -> templates.TemplateResponse:
    message_with_subject = str(subject) + str(message)
    simple_message = SimpleMessageCreate(
        name=name,
        email=email,
        message=message_with_subject,
    )
    subscriber = SubscriberCreate(email=email)
    try:
        create_simple_message(simple_message=simple_message, db=db)
        create_subscriber(subscriber, db=db)
    except IntegrityError:
        pass
    try:    
        background_tasks.add_task(
            send_message_received_email,
            str(email).lower()
        )
    except:
        pass
    finally:
        blogs_dict = await get_all_blogs_for_nav()
        
        return templates.TemplateResponse(
            str(
                Path(
                    'components',
                    'transitions',
                    'success.html'
                )
            ),
            {
                "request": request,
                "name": email,
                "all_blogs_dict": blogs_dict,
            }
        )


@general_pages_router.post("/submit-email", response_model=None)
async def submit_email_form(request: Request,
                            background_tasks: BackgroundTasks,
                            email: str = Form(...),
                            csrf_token: str = Form(...),
                            db: Session = Depends(get_db),
                            _: bool = Depends(validate_csrf_token),
                            ) -> templates.TemplateResponse:

    subscriber = SubscriberCreate(email=email)
    try:
        create_subscriber(subscriber, db=db)
    except IntegrityError:
        pass
    try:    
        background_tasks.add_task(
            send_welcome_email,
            str(email).lower()
        )
    except:
        pass
    finally:
        blogs_dict = await get_all_blogs_for_nav()
        
        return templates.TemplateResponse(
            str(
                Path(
                    'components',
                    'transitions',
                    'success.html'
                )
            ),
            {
                "request": request,
                "name": email,
                "all_blogs_dict": blogs_dict,
            }
        )


@general_pages_router.post("/submit-giveaway", response_model=None)
async def submit_giveaway_form(request: Request,
                               background_tasks: BackgroundTasks,
                               email: str = Form(...),
                               zip_code: str = Form(None),
                               csrf_token: str = Form(...),
                               db: Session = Depends(get_db),
                               _: bool = Depends(validate_csrf_token),
                               ) -> templates.TemplateResponse:
    if not zip_code:
        entrant = EntrantCreate(email=email)        
    else:
        entrant = EntrantCreate(email=email, zip_code=zip_code)
    try:
        create_entrant(entrant=entrant, db=db)
    except IntegrityError:
        pass
    subscriber = SubscriberCreate(email=email)
    try:
        create_subscriber(subscriber, db=db)
    except IntegrityError:
        pass
    try:    
        background_tasks.add_task(
            send_welcome_email,
            str(email).lower()
        )
    except:
        pass
    finally:
        blogs_dict = await get_all_blogs_for_nav()
        
        return templates.TemplateResponse(
            str(
                Path(
                    'components',
                    'transitions',
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
    background_tasks: BackgroundTasks,
    email: str = Form(...),
    db: Session = Depends(get_db)
) -> templates.TemplateResponse:

    background_tasks.add_task(
        remove_subscriber, 
        email, 
        db=db
    )
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


@general_pages_router.get("/{file_name:path}")
async def general_pages_route(
    request: Request,
    file_name: str,
):
    general_pages_path = Path(
        Path(__file__).parents[2],
        'templates',
        'general_pages', 
        f'{file_name}.html',
    )

    if not general_pages_path.is_file():
        raise HTTPException(
            status_code=404, 
            detail="Page requested not found"
        )
    template_path = Path(
        'general_pages',
        f'{file_name}.html',
    )
    blogs_dict = await get_all_blogs_for_nav()
    return templates.TemplateResponse(
        str(template_path),
        {
            "request": request,
            "all_blogs_dict": blogs_dict,
        },
    )