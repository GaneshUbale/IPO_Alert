

"""IPO alert bot using Selenium and Telegram notifications.
Tech stack used in this script:
- Python
- Selenium for browser automation
- requests for HTTP requests
- BeautifulSoup for HTML parsing
- Telegram Bot API for sending alerts

This script scrapes IPO subscription data from
https://www.investorgain.com/report/ipo-subscription-live/333/ipo/ using
Selenium and BeautifulSoup. It extracts IPO names, GMP percentages, and
closing dates, then sends alerts to Telegram when IPOs closing today or
tomorrow meet a minimum GMP threshold.
"""

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import re
import time 

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load from .env
load_dotenv()

# Read Telegram credentials from environment variables
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
CHANNEL_CHAT_ID = os.environ["TELEGRAM_CHANNEL_CHAT_ID"]

# URL to check
URL = "https://www.investorgain.com/report/ipo-gmp-live/331/ipo/"

# Set your alert condition
MIN_GMP = 10.0  # Minimum GMP %
DATE_TODAY = datetime.today().date()
DATE_TOMORROW = DATE_TODAY + timedelta(days=1)


def parse_close_date(date_str: str):
    """Parse close dates from formats like '21-Jul', '16-Jul', or '21-07-2025'."""
    normalized = re.sub(r"\b(st|nd|rd|th)\b", "", date_str.strip())
    normalized = normalized.replace(" ", "")

    yearful_formats = ["%d-%b-%Y", "%d-%B-%Y", "%d-%m-%Y"]
    yearless_formats = ["%d-%b", "%d-%B", "%d-%m"]

    for fmt in yearful_formats:
        try:
            return datetime.strptime(normalized, fmt).date()
        except ValueError:
            continue

    for fmt in yearless_formats:
        try:
            parsed_date = datetime.strptime(normalized, fmt).date()
            parsed_date = parsed_date.replace(year=DATE_TODAY.year)
            return parsed_date
        except ValueError:
            continue

    raise ValueError(f"Unsupported date format: {date_str}")


def extract_gmp_percentage(cell_text: str) -> str:
    """Extract the GMP percentage from a cell like '₹110 (25.94%) 80 ↓ / 117 ↑'."""
    if not cell_text:
        return "N/A"

    match = re.search(r"\(([-+]?\d+(?:\.\d+)?)%\)", cell_text)
    if match:
        return match.group(1)

    match = re.search(r"([-+]?\d+(?:\.\d+)?)%", cell_text)
    if match:
        return match.group(1)

    return "N/A"


def send_telegram_message(chat_id: str, msg: str, parse_mode: str = "Markdown") -> None:
    """Send a message via Telegram Bot API.

    Args:
        chat_id: Telegram chat id or channel id.
        msg: Message text to send. Supports Markdown or HTML when
            `parse_mode` is provided.
        parse_mode: Optional parse mode (e.g. "Markdown", "HTML"). Set to
            an empty string to disable parsing.

    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg}
    if parse_mode:
        payload["parse_mode"] = parse_mode

    try:
        response = requests.post(api_url, data=payload, timeout=10)
        response.raise_for_status()
        print(f"✅ Sent Telegram message to: {msg}")
    except requests.RequestException as exc:
        print(f"❌ Failed to send Telegram message: {exc}")
        raise

def fetch_ipo_data_with_selenium(url):    
    # Setup Chrome options
    options = Options()
    options.add_argument("--headless=new")  # Use modern headless mode
    options.add_argument("--window-size=1920,1080")

    # # Optional: spoof user-agent
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    # )

    # Create driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    try:
        # Now do whatever scraping logic you want here...
        # Scroll down to bottom and up to trigger lazy-loading
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)

        # Wait until the table with ID 'report_table' appears (max 15 seconds)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "reportTable"))
        )

        # Now parse page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', {'id': 'reportTable'})
        print("✅ IPO Table loaded.")
    
        ipo_data = []
        if table:
            rows = table.find_all('tr')
            for row in rows[2:]:  # Skip header and Search
                cols = row.find_all('td')
                # if len(cols) < 10:
                    # continue
                #First Column
                if len(cols) != 0: # It assure each row have data ('td')
                    firstCellText = cols[0].get_text(",", strip=True)
                    ipo_name = firstCellText.split(',')[0]
                    status = extract_gmp_percentage(cols[1].text)
                    fifthCellTextFromlast = cols[-5].get_text(",", strip=True)
                    close_date = fifthCellTextFromlast.split(',')[0]
                    ipo_data.append({
                        'IPO': ipo_name,
                        'Status': status,
                        'Close Date': close_date
                    })

    finally:
        driver.quit()

    return ipo_data

if __name__ == "__main__":
    print("✅ Running IPO checker...")
    try:
        data = fetch_ipo_data_with_selenium(URL)
        if len(data) == 0:
            print(f" ⛔️ No IPO found (Open/Closed)")
            send_telegram_message(CHAT_ID, f" ⛔️ No IPO found (Open/Closed), Need your immediate Attention! \n[Refer for more details]({URL})")
        message = f"🚀 **Upcoming IPO Alerts!**\n\n"
        count = 0
        gmps = ""
        for ipoRow in data:
            date_str = ipoRow['Close Date']
            closing_date = parse_close_date(date_str)
            if closing_date < DATE_TODAY:
                break
            if closing_date in [DATE_TODAY, DATE_TOMORROW]:
                gmps += ipoRow['Status'] + ","
            if float(ipoRow['Status']) >= MIN_GMP and closing_date in [DATE_TODAY, DATE_TOMORROW]:
                count += 1
                message += f"*{count} {ipoRow['IPO']}* \n🔹*GMP Percentile:* {ipoRow['Status']}% \n🔹*Closes on:* {ipoRow['Close Date']} "
                if closing_date == DATE_TODAY:
                    message += "i.e.🌞⏳ *Today* "
                else:
                    message += "i.e.🗓️ *Tomorrow* "
                message += "\n\n"
        #print(result)
        if count > 0:
            send_telegram_message(CHANNEL_CHAT_ID, message+ f"📢 *Don't miss out – apply before the deadlines!* \n[Refer for more details]({URL})")
        print(f"✅ Found {count} IPOs for your condition")
        if gmps != "":
            print(f" 🔘 There was few IPOs which don't have expected GMP and their gmps: {gmps}")
        print("✅ Check complete.")
    except Exception as e:
        print(f"❌ Error: {e}")
        send_telegram_message(CHAT_ID, f" ❌ Error: {e}, Need your immediate Attention! \n[Refer for more details]({URL})")
