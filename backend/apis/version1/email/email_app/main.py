#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
You must already have an instance of the email_server running on the
remote machine, as well as the Proton-Bridge mail client

Created on Sun Feb 19 09:26:48 2023

@author: dale
"""

import sys
from pathlib import Path
MAIN_DIR = Path(__file__).parent
if str(MAIN_DIR) not in sys.path:
    sys.path.append(str(MAIN_DIR))
if str(Path(MAIN_DIR, '__helpers__')) not in sys.path:
    sys.path.append(str(Path(MAIN_DIR, '__helpers__')))
    
import time
from ssh_login import return_ssh_connection
import commands_for_remote_email as commands


def transfer_files_to_remote_and_send_email(
        html_path,
        emails_path,
        from_email,
        url_str=None,
        png_path=None,
        pdf_path=None
    ):
    conn = return_ssh_connection()
    time.sleep(0.1)
    try:
        commands.transfer_file_to_remote(
            conn,
            html_path,
            '/home/opc/email_app/html_files',
        )
    except:
        commands.transfer_large_file_to_remote(
            conn,
            html_path,
            '/home/opc/email_app/html_files',
        )
    time.sleep(0.1)
    if png_path:
        commands.transfer_file_to_remote(
            conn,
            png_path,
            '/home/opc/email_app/email_png',
        )
        time.sleep(0.1)
    if pdf_path:
        commands.transfer_file_to_remote(
            conn,
            pdf_path,
            '/home/opc/email_app/pdf_attach',
        )
        time.sleep(0.1)
    c1, c2, c3 = commands.create_send_email_commands(
        html_path,
        emails_path,
        from_email,
        url_str=url_str,
        png_path=png_path,
        pdf_path=pdf_path,
    )
    commands.run_remote_command_in_shell(conn, c1)
    time.sleep(0.1)
    commands.run_remote_command_in_shell(conn, c2)
    time.sleep(0.1)
    commands.run_remote_command_in_shell(conn, c3)
    time.sleep(0.1)
    print('\nThe files have been successfully removed\n')

