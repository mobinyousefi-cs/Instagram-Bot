#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Instagram Bot – Automate Instagram Messages 
File: main.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
CLI entrypoint for sending Instagram DMs with optional delay or repeat.

Usage: 
python -m instagram_bot.main --to user1 user2 --message "Hello" --delay 10
python -m instagram_bot.main --to user1 --message "Ping" --repeat 900

Notes: 
- Educational purposes: may violate Instagram ToS. Use at your own risk.

===================================================================
"""
from __future__ import annotations

import argparse
import sys
from typing import List

from .automation.driver import make_driver
from .auth import login_and_persist
from .config import Settings
from .messaging import send_dm


def _parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="instagram-bot")
    p.add_argument("--to", nargs="+", required=True, help="Target username(s)")
    p.add_argument("--message", required=True, help="Message text to send")
    p.add_argument("--delay", type=float, default=0.0, help="Delay before first send (seconds)")
    p.add_argument(
        "--repeat",
        type=float,
        default=0.0,
        help="Repeat interval in seconds (0 = no repeat)",
    )
    return p.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    ns = _parse_args(sys.argv[1:] if argv is None else argv)

    cfg = Settings()
    cfg.validate()

    driver = make_driver(headless=cfg.headless)
    try:
        login_and_persist(driver, cfg)

        # Optional initial delay
        if ns.delay > 0:
            import time as _t

            _t.sleep(ns.delay)

        def _send_all() -> None:
            for user in ns.to:
                send_dm(driver, cfg.base_url, user, ns.message, delay_before_send=0)

        if ns.repeat > 0:
            from .scheduler import repeat_every

            repeat_every(ns.repeat, _send_all)
        else:
            _send_all()

        return 0
    finally:
        driver.quit()


if __name__ == "__main__":
    raise SystemExit(main())
