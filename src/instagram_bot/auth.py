#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Instagram Bot – Automate Instagram Messages 
File: auth.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Login workflow and cookie persistence.

Usage: 
from instagram_bot.auth import login_and_persist

Notes: 
- Uses cookie restore-first strategy to reduce logins.
- Update selectors if Instagram DOM changes.

===================================================================
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Iterable

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

from .config import Settings
from .exceptions import LoginError, SelectorNotFoundError
from .utils.selectors import SX


def _click_if_present(driver: WebDriver, xpath: str, timeout: float = 5.0) -> bool:
    try:
        el = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        el.click()
        return True
    except Exception:
        return False


def _restore_cookies(driver: WebDriver, base_url: str, cookie_path: Path) -> bool:
    if not cookie_path.exists():
        return False
    try:
        cookies = json.loads(cookie_path.read_text(encoding="utf-8"))
    except Exception:
        return False

    driver.get(base_url)
    for c in cookies:
        # Selenium expects domain-less cookies added after at least one navigation
        c.pop("sameSite", None)  # avoid invalid enum values
        try:
            driver.add_cookie(c)
        except Exception:
            pass
    driver.get(base_url)
    return True


def _save_cookies(driver: WebDriver, cookie_path: Path) -> None:
    cookies = driver.get_cookies()
    cookie_path.write_text(json.dumps(cookies, ensure_ascii=False, indent=2), encoding="utf-8")


def _wait_disappear(driver: WebDriver, xpath: str, timeout: float = 10.0) -> None:
    try:
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located((By.XPATH, xpath)))
    except Exception:
        pass


def login_and_persist(driver: WebDriver, cfg: Settings) -> None:
    """Ensure an authenticated session using cookie-restore-first strategy."""
    # Attempt cookie restore
    restored = _restore_cookies(driver, cfg.base_url, cfg.cookie_path)

    # Check if already logged in by hitting /direct/inbox/
    driver.get(f"{cfg.base_url}/direct/inbox/")
    time.sleep(2)
    if "/accounts/login" not in driver.current_url and "/challenge/" not in driver.current_url:
        return  # session is valid

    # Fresh login
    driver.get(f"{cfg.base_url}/accounts/login/")

    # Accept cookies if banner shown
    _click_if_present(driver, SX.ACCEPT_COOKIES_BTN, timeout=5)

    try:
        username_input = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, SX.USERNAME_INPUT))
        )
        password_input = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, SX.PASSWORD_INPUT))
        )
    except Exception as e:
        raise SelectorNotFoundError("Login inputs not found; DOM likely changed.") from e

    username_input.clear()
    username_input.send_keys(cfg.username)
    password_input.clear()
    password_input.send_keys(cfg.password)

    _click_if_present(driver, SX.LOGIN_BUTTON, timeout=10)

    # Wait for redirect or challenge
    WebDriverWait(driver, 30).until(
        lambda d: "/accounts/login" not in d.current_url
    )

    if "/challenge/" in driver.current_url:
        raise LoginError("Checkpoint/2FA challenge encountered. Complete manually then retry with cookies.")

    # Dismiss any "Save info" / "Turn on notifications" dialogs
    for _ in range(2):
        _click_if_present(driver, SX.NOT_NOW_BUTTON, timeout=5)
        time.sleep(1)

    # Persist cookies
    _save_cookies(driver, cfg.cookie_path)
