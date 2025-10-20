#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Instagram Bot – Automate Instagram Messages 
File: tests/test_smoke.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Minimal smoke tests that do not hit Instagram.

Usage: 
pytest -q

Notes: 
- These tests validate importability and basic helpers only.

===================================================================
"""
from __future__ import annotations

import importlib


def test_imports():
    assert importlib.import_module("instagram_bot")
    assert importlib.import_module("instagram_bot.config")
    assert importlib.import_module("instagram_bot.messaging")
    assert importlib.import_module("instagram_bot.auth")
