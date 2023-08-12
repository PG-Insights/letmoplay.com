#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 21:38:22 2023

@author: dale
"""

import base64
import pandas as pd
from html import escape
from pathlib import Path
import textwrap


class GetFiles:
    """ Class for managing the loading of values for the email client"""

    def __init__(self, file_path, *args, **kwargs):
        self._file_path = Path(file_path)
        if not self._file_path.is_file():
            raise ValueError(
                'The selected item is not an file or does not exist.'
            )
        else:
            self.filename = GetFiles.return_only_file_stem(file_path)
            self.name_wo_extension = GetFiles.return_only_file_name(
                file_path
            )
            self.data = GetFiles.check_file_and_return_values(
                file_path,
                *args,
                **kwargs
            )

    # The read_csv function will need to be modifed
    @staticmethod
    def read_csv_file(file_path, **kwargs) -> pd.DataFrame:
        return pd.read_csv(
            file_path, 
            usecols=['emails'], 
            **kwargs
        )

    # The read_excel function will need to be modifed
    @staticmethod
    def read_excel_file(file_path, **kwargs) -> pd.DataFrame:
        return pd.read_excel(
            str(file_path), 
            usecols=['emails'], 
            **kwargs
        )
    
    # This is fallback function if the filetype is not in SPECIFIED_IMPORTS
    @staticmethod
    def open_any_file_and_read_contents(file_path: str) -> str:
        with open(file_path, 'r') as f:
            any_file = f.readlines()
            f.close()
        
        temp_str = ' '.join(any_file)
        file_str = '\n'.join(textwrap.wrap(temp_str, width=998))
        return file_str

    # This will import any file and return a bytes string
    @staticmethod
    def read_file_as_bytes(file_path: str) -> bytes:
        with open(file_path, 'rb') as file:
            bytes_file = file.read()
        return bytes_file
    
    @staticmethod
    def return_only_file_stem(file_path):
        return Path(file_path).stem
    
    @staticmethod
    def return_only_file_name(file_path):
        return Path(file_path).name
    
    @staticmethod
    def _append_tracking_url_to_html_str(url_str, html_str):
        full_url = f'https://nochalknet.com/email_monitoring/{url_str}'
        return f'<img src="{full_url}" width="1" height="1" alt="">' + html_str
    
    @staticmethod
    def encode_html_str(html_str):
        escaped_html = escape(r"{}".format(html_str))
        return base64.b64encode(escaped_html.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def decode_html_str(html_str):
        return base64.b64decode(html_str.encode('utf-8')).decode('utf-8')

    # Update the dictionary when specific file getters are added to Class
    # The suffix should be the dictionary key and value is import function
    SPECIFIED_IMPORTS = {
        '.csv': read_csv_file,
        '.xlsx': read_excel_file,
        '.xls': read_excel_file,
        '.pdf': read_file_as_bytes,
        '.png': read_file_as_bytes,
    }

    @classmethod
    def check_file_and_return_values(cls, file_path, *args, **kwargs):
        file_suffix= Path(file_path).suffix
        if str(file_suffix) in GetFiles.SPECIFIED_IMPORTS.keys():
            get_func = GetFiles.SPECIFIED_IMPORTS.get(str(file_suffix))
        else:
            get_func = GetFiles.open_any_file_and_read_contents
        return get_func(file_path, *args, **kwargs)


if __name__ == '__main__':
    pass