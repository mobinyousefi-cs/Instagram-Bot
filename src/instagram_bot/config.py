#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Instagram Bot – Automate Instagram Messages 
File: config.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Centralized configuration and environment loading.

Usage: 
from instagram_bot.config import Settings
cfg = Settings()

Notes: 
- Loads .env via python-dotenv if present.
- Provides sane defaults for headless, base URL, etc.

===================================================================
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv(override=False)


@dataclass(frozen=True)
class Settings:
    username: str = os.getenv("IG_USERNAME", "")
    password: str = os.getenv("IG_PASSWORD", "")
    base_url: str = os.getenv("IG_BASE_URL", "https://www.instagram.com")
    headless: bool = os.getenv("IG_HEADLESS", "true").lower() == "true"
    cookie_path: Path = Path(os.getenv("IG_COOKIE_PATH", ".ig_session.json"))
    delay_min: float = float(os.getenv("IG_DEFAULT_DELAY_MIN", "1.0"))
    delay_max: float = float(os.getenv("IG_DEFAULT_DELAY_MAX", "2.5"))

    def validate(self) -> None:
        if not self.username or not self.password:
            raise ValueError(
                "IG_USERNAME and IG_PASSWORD must be set (see .env.example)."
            )
