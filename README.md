# 🤑 IPO Alert Bot (Telegram + GitHub Actions)

Get notified on Telegram when IPO meets your criteria:

- ✅ GMP ≥ 10%
- ✅ Closing Date is Today or Tomorrow

## 🚀 Setup Instructions

1. **Fork or clone this repo**

2. **Add your Telegram bot token & chat ID to GitHub Secrets**
   - `TELEGRAM_BOT_TOKEN`: From @BotFather
   - `TELEGRAM_CHAT_ID`: Use [this bot](https://t.me/userinfobot) to get your chat ID

3. **Customize your alert logic in `ipo_alert_bot_with_selenium.py`**  
   Change `MIN_GMP`, URL, etc. as needed

4. **GitHub Actions will run it daily at 9 AM IST**

---

Made with ❤️ for IPO hunters
