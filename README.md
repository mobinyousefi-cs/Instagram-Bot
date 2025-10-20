# Instagram Bot – Automate Instagram Messages (Python)

> **Educational use only.** Automating Instagram can violate Instagram’s Terms of Use and may lead to rate-limits or account bans. Use a test account, small volumes, and your own risk.

## ✨ Features
- Log in to Instagram Web with Selenium (optional headless)
- Cookie/session persistence to avoid frequent logins
- Send **scheduled** or **delayed** DMs to one or more users
- Randomized human-like delays and typing simulation
- Simple CLI: send once or schedule repeated jobs
- Clean, typed Python package structure with tests & CI

## 🧱 Project Structure
```
instagram-bot/
├─ src/
│  └─ instagram_bot/
│     ├─ __init__.py
│     ├─ main.py              # CLI entrypoint
│     ├─ config.py            # Settings & .env loading
│     ├─ exceptions.py
│     ├─ auth.py              # Login & session cookies
│     ├─ messaging.py         # DM send / typing simulation
│     ├─ scheduler.py         # Delayed & repeated jobs
│     └─ automation/
│        └─ driver.py         # Selenium driver factory
│     └─ utils/
│        ├─ __init__.py
│        └─ selectors.py      # Centralized DOM selectors
├─ tests/
│  └─ test_smoke.py
├─ .env.example
├─ .editorconfig
├─ .gitignore
├─ LICENSE
├─ pyproject.toml
└─ README.md
```

## ⚙️ Requirements
- Python 3.10+
- Google Chrome/Chromium + matching **chromedriver** (or use Selenium Manager auto-install)
- A test Instagram account

Install dependencies:
```bash
pip install -U pip
pip install -e .
```

## 🔐 Environment Variables
Copy `.env.example` to `.env` and fill:
```
IG_USERNAME=your_test_username
IG_PASSWORD=your_test_password
IG_HEADLESS=true
IG_BASE_URL=https://www.instagram.com
IG_COOKIE_PATH=.ig_session.json
IG_DEFAULT_DELAY_MIN=1.0
IG_DEFAULT_DELAY_MAX=2.5
```

## 🚀 Quick Start
Send a single DM to a user after a 10s delay:
```bash
python -m instagram_bot.main --to someuser --message "Hello from Selenium 🤖" --delay 10
```

Schedule a repeated message every 15 minutes (demo-safe frequency):
```bash
python -m instagram_bot.main --to someuser \
  --message "Ping from bot" --repeat 900
```

Send the same message to multiple users:
```bash
python -m instagram_bot.main --to user1 user2 user3 \
  --message "Hi! This is a test." --delay 5
```

Headless mode (default). To see the browser UI:
```bash
IG_HEADLESS=false python -m instagram_bot.main --to someuser --message "Hi"
```

## 🧠 How It Works (High-Level)
1. **Driver**: `automation/driver.py` configures a Chrome `webdriver` (headless by default) and a clean profile.
2. **Auth**: `auth.py` loads cookies if present, otherwise performs a credential login and saves session cookies.
3. **Selectors**: `utils/selectors.py` centralizes XPaths/CSS for UI elements used across the bot. If Instagram’s DOM changes, update in one place.
4. **Messaging**: `messaging.py` opens a DM thread for each target and simulates typing with randomized delays before submitting.
5. **Scheduler**: `scheduler.py` handles one-off delays and simple repeat intervals.

## 🧪 Testing
Run the basic test suite (no live DM is sent):
```bash
pytest -q
```

## 📦 Packaging
This project uses a modern `pyproject.toml` with:
- `ruff` + `black` formatting/linting
- `pytest` for tests
- `typing-extensions` (when needed)

## ⚠️ Disclaimer & Ethics
- Respect platform ToS and users’ consent.
- Keep rate low, add randomness and backoff.
- Prefer test accounts. Never spam or harass.

## 📜 License
MIT — see `LICENSE`.

## 👨‍💻 Author
Mobin Yousefi (GitHub: [mobinyousefi](https://github.com/mobinyousefi))

