#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Instagram Bot – Automate Instagram Messages 
File: scheduler.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Simple delay and repeat helpers for scheduling tasks.

Usage: 
from instagram_bot.scheduler import delay_then, repeat_every

Notes: 
- Lightweight on purpose; integrate APScheduler/Cron later if needed.

===================================================================
"""
from __future__ import annotations

import time
from typing import Callable


def delay_then(delay_seconds: float, fn: Callable[[], None]) -> None:
    if delay_seconds > 0:
        time.sleep(delay_seconds)
    fn()


def repeat_every(interval_seconds: float, fn: Callable[[], None], *, stop_after: float | None = None) -> None:
    start = time.time()
    while True:
        fn()
        if stop_after is not None and (time.time() - start) >= stop_after:
            break
        time.sleep(max(0.0, interval_seconds))
