#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Instagram Bot – Automate Instagram Messages 
File: messaging.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
DM message sending utilities with light human-like behavior (typing, delay).

Usage: 
from instagram_bot.messaging import send_dm

Notes: 
- DOM is fragile; adjust selectors in utils/selectors.py as IG changes.
- Uses direct URL to user thread when possible.

===================================================================
"""
from __future__ import annotations

import random
import time
from typing import Iterable

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

from .exceptions import MessageSendError, SelectorNotFoundError
from .utils.selectors import SX


def _human_delay(min_s: float, max_s: float) -> None:
    time.sleep(random.uniform(min_s, max_s))


def _open_dm_thread(driver: WebDriver, base_url: str, username: str) -> None:
    # Navigate to a direct compose for the username
    driver.get(f"{base_url}/direct/new/")

    # Type username in the recipient box and select first result
    try:
        input_box = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='queryBox']"))
        )
    except Exception as e:
        raise SelectorNotFoundError("DM recipient input not found.") from e

    input_box.clear()
    input_box.send_keys(username)
    _human_delay(0.5, 1.2)

    # Click the user in the dropdown list
    try:
        candidate = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//div[@role='dialog']//div[contains(@style,'cursor') and descendant::div[text()='@{username}'] or descendant::div[text()='{username}']]",
                )
            )
        )
        candidate.click()
    except Exception:
        # Fallback: choose the first result if exact match fails
        try:
            first = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "(//div[@role='dialog']//button)[1]"))
            )
            first.click()
        except Exception as e:  # noqa: PERF203
            raise SelectorNotFoundError("Cannot select recipient in compose list.") from e

    # Click Next to open the thread
    try:
        next_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='dialog']//div[text()='Next']/parent::button"))
        )
        next_btn.click()
    except Exception as e:
        raise SelectorNotFoundError("Next button in compose dialog not found.") from e

    # Wait for textbox to appear
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, SX.TEXTAREA_DM))
    )


def _type_text(driver: WebDriver, text: str, min_delay: float, max_delay: float) -> None:
    # Some IG inputs are contenteditable divs; use generic approach
    box = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, SX.TEXTAREA_DM))
    )
    for ch in text:
        box.send_keys(ch)
        _human_delay(min_delay, max_delay)


def send_dm(
    driver: WebDriver,
    base_url: str,
    username: str,
    message: str,
    delay_before_send: float | None = None,
    type_delay_min: float = 0.02,
    type_delay_max: float = 0.06,
    retries: int = 2,
) -> None:
    """Open (or compose) a DM thread and send a message."""
    _open_dm_thread(driver, base_url, username)

    if delay_before_send and delay_before_send > 0:
        time.sleep(delay_before_send)

    # Type text like a human
    _type_text(driver, message, type_delay_min, type_delay_max)

    # Press Enter to send (typical for IG). If fails, click Send button.
    box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, SX.TEXTAREA_DM))
    )

    for attempt in range(retries + 1):
        try:
            box.send_keys(Keys.ENTER)
            # Simple confirmation: wait for input to clear / last bubble to appear
            time.sleep(1.5)
            return
        except Exception:
            # Fallback: try clicking a Send button
            try:
                send_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, SX.SEND_BUTTON))
                )
                send_btn.click()
                time.sleep(1.5)
                return
            except Exception:
                if attempt >= retries:
                    raise MessageSendError("Failed to send DM after retries.")
                time.sleep(1.0 + attempt)
