# Mechanical Pamuk Bot

This bot posts a random quote to X (Twitter) on a schedule using Selenium + Chrome in headless mode.

## What this is

- **pamuk_bot.py** – the main script that opens X and posts a random line from `quotes.txt`.
- **quotes.txt** – one quote per line (UTF-8). The script picks a random non-empty line each run.
- **twitter_cookies.pkl** – your saved login session for X. This file is **not** in Git; you create it on each machine.
- **requirements.txt** – the Python packages/versions to install.
- **pamuk_wrapper.sh** – tiny shell script cron calls; it activates the venv and runs the bot. (We’ll create it.)
- **venv/** – your Python virtual environment. Not in Git; recreate per machine.
- **cron.log** – log output from scheduled runs. Not in Git; created at runtime.

## Prerequisites

- A machine with **Python 3.9+**.
- **Google Chrome** or **Chromium** installed.
- Internet access (to load X and to let `webdriver-manager` download the correct ChromeDriver the first time).

## First-time setup (new machine)

> Do all commands in a Terminal on the new machine.

1. **Clone this repo**
   ```bash
   git clone <YOUR-REPO-URL>.git
   cd mechanical_pamuk

