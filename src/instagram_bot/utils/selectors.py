#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Instagram Bot – Automate Instagram Messages 
File: utils/selectors.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Centralized selectors (XPaths/CSS) used by the bot. Instagram’s DOM
changes often—update these in one place.

Usage: 
from instagram_bot.utils.selectors import SX

Notes: 
- Prefer robust XPaths and data-testid when available.
- Keep names semantic.

===================================================================
"""
from __future__ import annotations


class SX:
    # Login page
    ACCEPT_COOKIES_BTN = "//button[contains(., 'Only allow essential cookies') or contains(., 'Allow all cookies') or contains(., 'Accept')]"
    USERNAME_INPUT = "//input[@name='username']"
    PASSWORD_INPUT = "//input[@name='password']"
    LOGIN_BUTTON = "//button[@type='submit' and descendant::*[text()='Log in' or text()='Log In']]"

    # Save login info / notifications popups
    NOT_NOW_BUTTON = "//button[contains(., 'Not Now')]"

    # Messaging (DM)
    # Open chat compose or navigate to thread: we'll use a direct URL to /direct/t/ or /direct/new/
    TEXTAREA_DM = "//textarea|//div[@role='textbox']"
    SEND_BUTTON = "//button//*[name()='svg' and @aria-label='Send']|//button[@type='submit' and contains(., 'Send')]"

    # Generic
    ANY_SPINNER = "//*[self::div or self::span][contains(@class,'spinner') or contains(@class,'loading')]"
