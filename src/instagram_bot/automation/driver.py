#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Instagram Bot – Automate Instagram Messages 
File: automation/driver.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Selenium WebDriver factory with sane defaults and headless support.

Usage: 
from instagram_bot.automation.driver import make_driver

Notes: 
- Uses Selenium 4 Service and built-in driver manager when available.
- Disables automation flags as much as possible (still detectable by IG).

===================================================================
"""
from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def make_driver(headless: bool = True) -> webdriver.Chrome:
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,1200")
    # Some steadiness
    opts.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    opts.add_experimental_option("useAutomationExtension", False)

    # Selenium Manager will fetch the correct ChromeDriver automatically
    service = Service()
    driver = webdriver.Chrome(service=service, options=opts)

    # Fingerprint light mitigations
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": (
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
            )
        },
    )
    return driver
