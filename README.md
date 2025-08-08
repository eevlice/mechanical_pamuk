# Mechanical Pamuk Bot

Posts a random quote to **X (Twitter)** on a schedule using **Selenium + Chrome** in headless mode.

---

## What’s in this folder

Tracked in Git (safe to share):
- **`pamuk_bot.py`** → main script that opens X and posts a random line from `quotes.txt`.
- **`quotes.txt`** → one quote per line (UTF‑8). Blank lines are skipped. (Keep or replace with your own content.)
- **`requirements.txt`** → exact Python packages/versions to install.
- **`README.md`** → this guide.
- **`save_cookies.py`** → helper to log in once and save cookies for headless runs.
- **`pamuk_wrapper.sh`** → tiny script cron uses to activate the venv and run the bot. (Create it with the command below.)

Ignored by Git (kept local only):
- **`twitter_cookies.pkl`** → your saved X login session (private; re-create per machine).
- **`venv/`** → Python virtual environment (rebuild any time from `requirements.txt`).
- **Logs** → `cron.log`, `wrapper_test.log`.
- **Debug files** → `debug_page.html`, `debug_screenshot.png` (if you generate them).

> These are listed in `.gitignore` to keep secrets/junk out of Git.

---

## Prerequisites

- **Python 3.9+**
- **Google Chrome** (macOS) or **Chromium** (Linux/Raspberry Pi)
- Internet access (so `webdriver-manager` can fetch the right ChromeDriver the first time)

> **macOS note:** In `pamuk_bot.py` the Chrome binary is set to  
> `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`.  
> On Linux/Raspberry Pi you can comment that line out or set it to your Chromium path.

---

## First-time setup on a new machine

Do these in a Terminal.

### 1) Get the code

If using GitHub:
```bash
git clone <YOUR-REPO-URL>.git
cd mechanical_pamuk
```

If you copied the folder some other way, just `cd` into it.

### 2) Create a virtual environment & install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

### 3) Provide `quotes.txt`
- Put your `quotes.txt` in this folder (one quote per line, UTF‑8).  
- At least one non-empty line must exist.

### 4) Save X.com cookies once (per machine)
Create `save_cookies.py` with this content (already in repo; re-copy if needed):

```python
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Headed on purpose: you'll see a real browser to log in.
opts = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=opts)

driver.get("https://x.com/login")
print("Log in in the browser window, then return here and press ENTER…")
input()

with open("twitter_cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)
print("Saved cookies to twitter_cookies.pkl")

driver.quit()
```

Run it:
```bash
source venv/bin/activate
python save_cookies.py
deactivate
```
This creates **`twitter_cookies.pkl`** in the project folder.

### 5) Test a manual run
```bash
source venv/bin/activate
python pamuk_bot.py
deactivate
```
You should see output ending with **“✅ Tweet sent!”**.  
If it fails, re-check cookies, `quotes.txt`, and your Chrome/Chromium install.

---

## Scheduling with cron (automatic runs)

We use a small wrapper so cron can activate your venv and run the bot from anywhere.

### 1) Create the wrapper **in this folder**
```bash
cat > pamuk_wrapper.sh << 'EOF'
#!/usr/bin/env bash
# Activate the venv inside this project folder
source "$(dirname "$0")/venv/bin/activate"
# Run the bot and append logs to cron.log (in this folder)
python "$(dirname "$0")/pamuk_bot.py" >> "$(dirname "$0")/cron.log" 2>&1
EOF
chmod +x pamuk_wrapper.sh
```

### 2) Install a cron schedule

Open your crontab with nano (simple editor):
```bash
EDITOR=nano crontab -e
```

Add **one** of these lines (replace the path with the absolute path to this folder):

- **Every 15 minutes** (at :00, :15, :30, :45):
```
*/15 * * * * /full/path/to/mechanical_pamuk/pamuk_wrapper.sh
```

- **Once an hour at HH:00**:
```
0 * * * * /full/path/to/mechanical_pamuk/pamuk_wrapper.sh
```

Save (**Ctrl+O**, Enter), exit (**Ctrl+X**), then confirm:
```bash
crontab -l
```

### 3) Check logs
```bash
tail -n 50 /full/path/to/mechanical_pamuk/cron.log
```

> **Sleep note:** cron only runs when the machine is **awake**. Keep it awake at run times (power settings or `caffeinate`).  
> Example to keep awake for 2 hours: `caffeinate -s -t 7200`

---

## Updating content

- Edit `quotes.txt` any time; the bot reads it fresh each run.
- If cookies expire, re-run `save_cookies.py` to refresh `twitter_cookies.pkl`.

---

## Troubleshooting quick hits

- **Headless “browser not supported” page** → The provided `pamuk_bot.py` already spoofs a real UA and hides automation flags. Make sure you’re using this repo’s script.
- **Timeout waiting for compose box** → Cookies missing/expired; re-run `save_cookies.py` and ensure you’re navigating to `https://x.com/compose/tweet`.
- **Cron didn’t run** → Machine may have been asleep. Add a “heartbeat” to confirm cron is alive:
  ```bash
  EDITOR=nano crontab -e
  ```
  Add:
  ```
  * * * * * echo "cron alive at $(date)" >> ~/cron_test.log 2>&1
  ```
  Wait 2 minutes then:
  ```bash
  tail -n 5 ~/cron_test.log
  ```
- **ModuleNotFoundError in cron** → Ensure the wrapper activates the venv before running the bot.

---

## Moving/Backing up the project (one-file archive)

Create a single archive that includes everything in this folder **plus** the wrapper:
```bash
cd ~/bots
tar czf mechanical_pamuk.tar.gz mechanical_pamuk pamuk_wrapper.sh
```
Restore on another machine:
```bash
mkdir -p ~/bots && cd ~/bots
tar xzf mechanical_pamuk.tar.gz
cd mechanical_pamuk
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt || pip install selenium webdriver-manager
deactivate
# Re-generate twitter_cookies.pkl with save_cookies.py
```

---

## What not to commit (already in `.gitignore`)

```
venv/
twitter_cookies.pkl
*.log
debug_page.html
debug_screenshot.png
__pycache__/
*.pyc
.DS_Store
pamuk_bot_temp_profile/
```

---

## Security & privacy

- Never commit `twitter_cookies.pkl`. Anyone with those cookies can post as you.
- Prefer a **private** GitHub repo if your `quotes.txt` is not for public eyes.
