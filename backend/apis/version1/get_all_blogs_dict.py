#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 21:58:32 2023

@author: dale
"""

from pathlib import Path

def get_all_blogs_dict(dir_path: str) -> list:
    all_blogs_dict = {}
    blogs_dir = [Path(yr_dir) for yr_dir in Path(dir_path).iterdir()]
    for years_dir in blogs_dir:
        year_key = Path(years_dir).stem
        if year_key not in all_blogs_dict:
            all_blogs_dict[year_key] = {}
        for months_dir in Path(years_dir).iterdir():
            months_key = Path(months_dir).stem
            if months_key not in all_blogs_dict[year_key].keys():
                all_blogs_dict[year_key][months_key] = []
            for blog in Path(months_dir).iterdir():
                all_blogs_dict[year_key][months_key].append(Path(blog).stem)
    return all_blogs_dict
