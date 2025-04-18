import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Read Telegram credentials from environment variables
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# URL to check
URL = "https://www.investorgain.com/report/ipo-subscription-live/333/ipo/"

# Set your alert condition
MIN_GMP = 25  # Minimum GMP %
DATE_TODAY = datetime.today().date()
DATE_TOMORROW = DATE_TODAY + timedelta(days=1)

def send_telegram_message(msg):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    response = requests.post(api_url, data=payload)
    response.raise_for_status()

def check_ipo_page():
    response = requests.get(URL, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")
    
    ipo_cards = soup.select(".iporpt-box")

    for card in ipo_cards:
        name = card.select_one(".grey14, .text-ellipsis").text.strip()
        status = card.select_one("td:contains('GMP') ~ td").text.strip()
        date_text = card.select_one("td:contains('Closing Date') ~ td").text.strip()

        gmp_value = int(''.join(filter(str.isdigit, status)))
        closing_date = datetime.strptime(date_text, "%d-%b-%Y").date()

        if gmp_value >= MIN_GMP and closing_date in [DATE_TODAY, DATE_TOMORROW]:
            message = f"📈 *IPO Alert*\n\n*{name}*\nGMP: {gmp_value}%\nClosing: {closing_date.strftime('%d %b %Y')}"
            send_telegram_message(message)

if __name__ == "__main__":
    print("Running IPO checker...")
    try:
        check_ipo_page()
        print("✅ Check complete.")
    except Exception as e:
        print(f"❌ Error: {e}")
