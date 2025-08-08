import random
import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 0. Base directory for all your bot files
BASE_DIR = "/Users/erkamevlice/bots/mechanical_pamuk"

# 1. Load a random quote from quotes.txt
with open(f"{BASE_DIR}/quotes.txt", encoding="utf-8") as f:
    quotes = [line.strip() for line in f if line.strip()]
quote = random.choice(quotes)

# 2. Build ChromeOptions for headless with UA spoofing
opts = webdriver.ChromeOptions()
opts.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
opts.add_argument(
    "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/139.0.7258.67 Safari/537.36"
)
opts.add_argument("--headless=new")
opts.add_argument("--disable-blink-features=AutomationControlled")
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
opts.add_experimental_option("useAutomationExtension", False)
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--window-size=1280,1024")
opts.add_argument("--disable-gpu")

# 3. Start ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=opts)

# 4. Navigate to x.com and inject saved cookies
driver.get("https://x.com")
with open(f"{BASE_DIR}/twitter_cookies.pkl", "rb") as f:
    for cookie in pickle.load(f):
        cookie.pop("domain", None)
        cookie.pop("sameSite", None)
        driver.add_cookie(cookie)

# 5. Go to the compose tweet screen
print("🟡 Navigating to x.com/compose/tweet…")
driver.get("https://x.com/compose/tweet")

try:
    wait = WebDriverWait(driver, 20)

    # 6. Wait for and fill the tweet box
    print("🟡 Waiting for tweet box…")
    tweet_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="textbox"]')))
    tweet_box.click()
    tweet_box.send_keys(quote)
    time.sleep(1)

    # 7. Try keyboard shortcuts
    tweet_box.send_keys(Keys.COMMAND, Keys.ENTER)
    tweet_box.send_keys(Keys.CONTROL, Keys.ENTER)
    time.sleep(1)

    # 8. Fallback: click the Tweet button via JS
    print("🟡 Looking for Tweet button…")
    button = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        'div[data-testid="tweetButton"], div[data-testid="tweetButtonInline"]'
    )))
    driver.execute_script("arguments[0].click();", button)

    print("✅ Tweet sent!")

except Exception as e:
    print("❌ Error tweeting:", repr(e))

# 9. Clean up
time.sleep(5)
driver.quit()
