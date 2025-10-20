#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Instagram Bot – Automate Instagram Messages 
File: __init__.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Package initializer. Exposes high-level APIs for login and messaging.

Usage: 
from instagram_bot import send_message_once

Notes: 
- Keeps the public surface minimal and typed.

===================================================================
"""
from __future__ import annotations

from .auth import login_and_persist
from .messaging import send_dm
from .scheduler import delay_then, repeat_every

__all__ = [
    "login_and_persist",
    "send_dm",
    "delay_then",
    "repeat_every",
]
