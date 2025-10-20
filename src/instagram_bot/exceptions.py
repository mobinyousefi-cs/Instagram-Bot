#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Instagram Bot – Automate Instagram Messages 
File: exceptions.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Custom exceptions for the package.

Usage: 
raise LoginError("...")

Notes: 
- Keep exception taxonomy small and meaningful.

===================================================================
"""
from __future__ import annotations


class InstagramBotError(Exception):
    """Base exception for the instagram_bot package."""


class LoginError(InstagramBotError):
    """Raised when login fails (e.g., invalid credentials or DOM changes)."""


class SelectorNotFoundError(InstagramBotError):
    """Raised when a critical DOM element cannot be located."""


class MessageSendError(InstagramBotError):
    """Raised when sending a DM fails after retries."""
