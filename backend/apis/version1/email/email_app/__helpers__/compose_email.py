import os
import time
import sys
import smtplib
from pathlib import Path
from dotenv import load_dotenv
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
if str(Path(__file__).parents[0]) not in sys.path:
    sys.path.append(str(Path(__file__).parents[0]))
    sys.path.append(str(Path(__file__).parents[1]))
from get_files import GetFiles

load_dotenv()


class ComposeEmail:
    
    _vm_email_path = Path('/', 'home', 'opc', 'email_app')
    _ip = '127.0.0.1'
    _port = 1025
    
    def __init__(
            self,
            html_path: str,
            emails_list_or_path: str,
            from_email: str = 'letmoplay@letmoplay.com',
            *,
            url_str: str = 'welcome_email',
            pdf_path: str = None,
            png_path: str = None):
        self.msg = MIMEMultipart()
        self.from_email = from_email
        self.emails_list_or_path = emails_list_or_path
        self.emails_list = self._set_emails_list()
        self.html_obj = GetFiles(html_path)
        self.email_subject = self.html_obj.filename
        self.html_obj.data = GetFiles._append_tracking_url_to_html_str(
            url_str,
            self.html_obj.data
        )
        if png_path:
            self.png_path = Path(png_path)
        else:
            self.png_path = None
        
        if pdf_path:
            self.pdf_path = Path(pdf_path)
        else:
            self.pdf_path = None
        
        self.composed_email = self.compose_html_email()
        
    def _set_emails_list(self) -> list:
        try:
            return GetFiles(self.emails_list_or_path).data
        except ValueError:
            return [self.emails_list_or_path]
        
    def compose_html_email(self) -> MIMEText:   
        self.msg['From'] = self.from_email
        self.msg['To'] = self.from_email
        self.msg['Subject'] = self.email_subject
        self._add_html_to_msg()
        if self.png_path:
            self.add_png_to_email()
        if self.pdf_path:
            self.add_pdf_to_email()
        return self.msg.as_string()
    
    def _add_html_to_msg(self):
        mime_html = MIMEText(self.html_obj.data, 'html')
        self.msg.attach(mime_html)

    def add_png_to_email(self):
        img_html = MIMEText('<img src="cid:image1">', 'html')
        self.msg.attach(img_html)
        image = MIMEImage(GetFiles(self.png_path).data)
        image.add_header('Content-ID', '<image1>')
        self.msg.attach(image)
        
    def get_pdf_for_email(self) -> bytes:
        try:
            pdf_obj = GetFiles(self.pdf_path)
            payload = MIMEBase(
                'application', 
                'octate-stream', 
                Name=f'{pdf_obj.filename}.pdf',
            )
            payload.set_payload(pdf_obj.data)
            encoders.encode_base64(payload)
            payload.add_header(
                'Content-Decomposition', 
                'attachment', 
                filename=f'{pdf_obj.filename}.pdf',
            )
            return payload
        except Exception as e:
            print('\nError:', e, '\n')
            return None
        
    def add_pdf_to_email(self):
        pdf_payload = self.get_pdf_for_email()
        self.msg.attach(pdf_payload)
    
    def get_unique_emails_from_series_or_list(self) -> list:
        if isinstance(self.emails_list, list):
            no_dups = set(self.emails_list)
            no_dups_list = list(no_dups)
        else:
            no_dups = self.emails_list['emails'].unique()
            no_dups_list = no_dups.tolist()
        return no_dups_list
    
    def send_email_func(self) -> None:  
        emails_list = self.get_unique_emails_from_series_or_list()
        with smtplib.SMTP(self._ip, self._port) as smtp:
            smtp.starttls()
            smtp.login(os.environ.get('UNAME'), os.environ.get('PASS'))
            time.sleep(.1)
            smtp.sendmail(
                self.from_email, 
                [self.from_email] + emails_list, 
                self.composed_email
            )
            smtp.quit()

