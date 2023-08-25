#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 18:08:28 2023

@author: dale
"""


from fabric import Connection
from pathlib import Path
from io import BytesIO
import sys
import os


if str(Path(__file__).parent) not in sys.path:
    sys.path.append(str(Path(__file__).parent))
from __helpers__.compose_email import ComposeEmail



def transfer_file_to_remote(
        conn: Connection,
        file_path: str,
        save_path: str) -> None:
    with conn:
        conn.put(file_path, save_path)
        

def transfer_large_file_to_remote(
        conn: Connection, 
        file_path: str, 
        save_path: str) -> None:
    chunk_size = 1024 * 256
    file_size = os.path.getsize(file_path)
    file_name = Path(file_path).name
    with open(file_path, 'rb') as f:
        for i in range(0, file_size, chunk_size):
            chunk = f.read(chunk_size)
            remote_file_path = str(
                Path(
                    save_path, 
                    
                    f'part{i // chunk_size}'
                )
            )
            conn.put(BytesIO(chunk), remote_file_path)
    conn.run(
        f'cat {save_path}/part* > {save_path}/{file_name} && rm {save_path}/part*'
    )


def run_remote_command_in_shell(
        conn: Connection,
        command_str: str) -> None:
    with conn:
        conn.run(command_str, asynchronous=False)


def create_send_email_commands(
        html_path: str,
        to_email: str,
        from_email: str = 'letmoplay@letmoplay.com',
        *,
        url_str: str = 'welcome_email',
        png_path: str=None,
        pdf_path: str=None,) -> tuple:
    main_dir = ComposeEmail._vm_email_path  # this needs to match remote box
    html_dir = Path(main_dir, 'html_files')
    html_path = Path(html_dir, Path(html_path).name)
    
    command_activate_venv_command = " ".join(
        [
            'source',
            f'{str(main_dir)}/venv/bin/activate'
         ]
    )
    command_send_html_email = [
        'python3.11',
        f'"{str(main_dir)}/__helpers__/compose_email.py"',
        f'"{str(html_path)}"',
        f'"{str(to_email)}"',
        f'{str(from_email)}',
    ]
        
    command_clear_folders = [
        'rm',
        f'"{str(html_path)}"',
    ]
    
    send_command = [
        '--url_str'
        f' "{str(url_str)}"'
    ]
    command_send_html_email = command_send_html_email + send_command

    if png_path:
        png_dir = Path(main_dir, 'email_png')
        png_path = Path(png_dir, Path(png_path).name)
        send_command = [
            '--png_path'
            f' "{str(png_path)}"'
        ]
        clear_command = [
            '&&',
            'rm',
            f'"{str(png_path)}"'
        ]
        command_send_html_email = command_send_html_email + send_command
        command_clear_folders = command_clear_folders + clear_command
        
    if pdf_path:
        pdf_dir = Path(main_dir, 'pdf_attach')
        pdf_path = Path(pdf_dir, Path(pdf_path).name)
        send_command = [
            '--pdf_path'
            f' "{str(pdf_path)}"'
        ]
        clear_command = [
            '&&',
            'rm',
            f'"{str(pdf_path)}"'
        ]
        command_send_html_email = command_send_html_email + send_command
        command_clear_folders = command_clear_folders + clear_command
    command_send_html_email_str = " ".join(command_send_html_email)
    command_clear_folders_str = " ".join(command_clear_folders)
    return (
        command_activate_venv_command,
        command_send_html_email_str,
        command_clear_folders_str,

    )

if __name__ == '__main__':
    vm_command = create_send_email_commands(
        'test-email',
        'test-path.html',
        png_path='test-path.png',
        pdf_path='test-path.pdf'
    )