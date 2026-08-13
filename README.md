# 🤑 IPO Alert Bot (Telegram + GitHub Actions)

Get notified on Telegram when IPO meets your criteria:

- ✅ GMP ≥ 10%
- ✅ Closing Date is Today or Tomorrow

## 📲 Join Telegram Channel

Join the IPO alerts channel here:

- Telegram link: [Ganesh's IPO Alert Channel](https://t.me/+elf_KdkTUnU0ODA9) 
- OR Scan the QR code below to join:

  ![Telegram Channel QR](./resources/telegram_qr_code.jpeg)

## 🚀 Setup Instructions

1. **Fork or clone this repo**
2. **Add your Telegram bot token & chat ID to GitHub Secrets**

   - `TELEGRAM_BOT_TOKEN`: From @BotFather
   - `TELEGRAM_CHAT_ID`: Use [this bot](https://t.me/userinfobot) to get your chat ID
3. **Customize your alert logic in `ipo_alert_bot_with_selenium.py`**Change `MIN_GMP`, URL, etc. as needed
4. **GitHub Actions will run it daily at 9 AM IST**

---

Made with ❤️ for IPO hunters
