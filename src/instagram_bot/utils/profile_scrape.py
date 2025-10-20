#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Instagram Bot – Automate Instagram Messages 
File: utils/profile_scrape.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Lightweight helper using requests + BeautifulSoup to fetch basic
public profile info (if available) to sanity-check target usernames
before attempting a DM.

Usage: 
from instagram_bot.utils.profile_scrape import fetch_profile_title

Notes: 
- Instagram heavily rate-limits and may block requests. Use sparingly.
- Many profiles are private; treat this as a best-effort check.

===================================================================
"""
from __future__ import annotations

from typing import Optional
import requests
from bs4 import BeautifulSoup


def fetch_profile_title(base_url: str, username: str, timeout: float = 8.0) -> Optional[str]:
    url = f"{base_url.rstrip('/')}/{username.strip('/')}/"
    try:
        r = requests.get(url, timeout=timeout, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        })
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.find("title")
        return title.text.strip() if title else None
    except Exception:
        return None
