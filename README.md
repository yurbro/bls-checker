<div align="center">

# 🇪🇸 BLS Spain UK — Visa Slot Checker

**Never miss a visa appointment again.**

Monitors the BLS Spain UK booking page every 5 minutes and fires an instant Telegram alert the moment a slot opens up.

🌐 [English](./README.md) | [中文](./README_CN.md)

---

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Free-2088FF?style=flat-square&logo=github-actions&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=flat-square&logo=telegram&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## ✨ Features

- 🔍 **Auto-detects** available appointment slots on BLS Spain UK
- 📲 **Instant Telegram alerts** the moment a slot appears
- ⏱️ **Runs every 5 minutes** via GitHub Actions — completely free
- 🛡️ **Graceful error handling** — timeouts, blocks, and failures won't crash the bot
- 🔒 **No credentials stored** — all secrets managed via GitHub environment variables

---

## 🚀 Quick Start

### Step 1 — Create a Telegram Bot

1. Open Telegram and search for **[@BotFather](https://t.me/BotFather)**
2. Send `/newbot` and follow the prompts
3. Copy your **Bot Token** — it looks like `123456789:AABBccDDee...`
4. Start a conversation with your new bot by sending `/start`
5. Get your **Chat ID** by opening this URL in your browser:
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
   Look for the `"id"` field in the response JSON

### Step 2 — Fork or Upload to GitHub

1. Fork this repo **or** create a new private repository
2. Upload all files including the `.github/` folder

### Step 3 — Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Value |
|--------|-------|
| `TELEGRAM_BOT_TOKEN` | Your bot token |
| `TELEGRAM_CHAT_ID` | Your chat ID (numbers only) |

### Step 4 — Enable & Test

1. Click the **Actions** tab in your repository
2. Select **BLS Spain Slot Checker** → click **Run workflow**
3. Within 30 seconds, your Telegram should receive a startup message ✅

---

## 📁 Project Structure

```
bls-checker/
├── checker.py                 # Core detection script
├── requirements.txt           # Python dependencies
├── .github/
│   └── workflows/
│       └── checker.yml        # GitHub Actions schedule (every 5 min)
└── README.md
```

---

## ⚙️ Configuration

All config lives at the top of `checker.py`:

```python
# Target URL — update if BLS changes their booking page
TARGET_URL = "https://blsspainuk.com/appointment/"

# Slot found if any of these appear on the page
SLOT_KEYWORDS = ["available", "select", "choose", "book", "confirm"]

# No slot if any of these appear
NO_SLOT_KEYWORDS = ["no appointment", "no slot", "fully booked", "unavailable"]
```

### Change check frequency

Edit the cron expression in `.github/workflows/checker.yml`:

```yaml
- cron: "*/5 * * * *"    # Every 5 minutes (recommended)
- cron: "*/10 * * * *"   # Every 10 minutes
```

> **Note:** 5 minutes is GitHub Actions' minimum interval.

---

## 💰 Completely Free

| Service | Cost |
|---------|------|
| GitHub Actions | 2,000 min/month free · this bot uses ~1,440 min/month |
| Telegram Bot API | Free, no limits |

---

## 🔧 Run Locally

```bash
# Clone the repo
git clone https://github.com/your-username/bls-checker.git
cd bls-checker

# Install dependencies
pip install -r requirements.txt

# Set your credentials
export TELEGRAM_BOT_TOKEN="your-token"
export TELEGRAM_CHAT_ID="your-chat-id"

# Run once
python checker.py
```

To run continuously, uncomment the `while True` loop at the bottom of `checker.py`.

---

## ⚠️ Disclaimer

- This tool is for **personal use only**. Do not run at abusive frequencies.
- When a slot is detected, you must **complete the booking manually** — the bot does not auto-submit any forms.
- If BLS adds login requirements or heavy JavaScript, the script may need to be upgraded to [Playwright](https://playwright.dev/).

---

## 🤝 Contributing

PRs welcome! Some ideas for future improvements:

- [ ] Playwright support for JS-rendered pages
- [ ] Support for multiple appointment types
- [ ] Discord / WeChat notification options
- [ ] Docker deployment support

---

<div align="center">

Made with ☕ for everyone struggling to get a Spain visa appointment in London.

**If this saved you time, consider giving it a ⭐**

</div>
