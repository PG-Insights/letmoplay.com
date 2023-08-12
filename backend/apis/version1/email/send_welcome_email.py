# -*- coding: utf-8 -*-

import sys
from pathlib import Path

if str(Path(__file__).parent) not in sys.path:
    sys.path.append(str(Path(__file__).parent))
    sys.path.append(str(Path(Path(__file__).parent, 'email_app')))
    
from email_app.main import transfer_files_to_remote_and_send_email

def send_welcome_email(email_str: str) -> None:
    dir_path = Path(Path(__file__).parent, 'email_app')
    transfer_files_to_remote_and_send_email(
        str(Path(dir_path, 'html_files', 'Welcome to the Let MO Play Team.html')),
        email_str,
        'letmoplay@letmoplay.com',
        url_str='welcome_email',
    )
