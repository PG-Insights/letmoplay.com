#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 09:41:54 2023

@author: dale
"""

import os
from pathlib import Path
from fabric import Connection
from dotenv import load_dotenv

load_dotenv()


def return_ssh_connection(
        ssh_filename=os.environ.get('SSH_PATH'),
        hostname = os.environ.get('VM_HOST')
        ) -> Connection:
    # Login to the remote machine and return connection
    path_to_ssh = Path(Path(__file__).parent, ssh_filename)
    return Connection(
        hostname, 
        user='opc', 
        connect_kwargs={'key_filename': str(path_to_ssh)}
    ) 


if __name__ == '__main__':
    conn = return_ssh_connection()