<div align="center">

# 🇪🇸 BLS Spain UK — Visa Slot Checker

**Never miss a visa appointment again.**

Uses a real browser (Playwright) to log into BLS, check the London Tourist Visit booking calendar, and fire an instant Telegram alert the moment a slot opens up.

🌐 [English](./README.md) | [中文](./README_CN.md)

---

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Headless_Browser-2EAD33?style=flat-square&logo=playwright&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Free-2088FF?style=flat-square&logo=github-actions&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=flat-square&logo=telegram&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## ✨ Features

- 🌐 **Real browser automation** — Uses Playwright (headless Chromium) to handle login, JavaScript rendering, and dynamic content
- 🔐 **Logs into your BLS account** — Navigates the actual booking flow to check for available dates
- 📲 **Instant Telegram alerts** with screenshot when a slot appears
- ⏱️ **Runs every 5 minutes** via GitHub Actions — completely free
- 📸 **Debug screenshots** — Every run saves screenshots, uploaded as GitHub Actions artifacts
- 🛡️ **Graceful error handling** — Site down, login failures, and timeouts are all handled cleanly
- 🔒 **Secure** — All credentials stored in GitHub Secrets, never in code

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

### Step 2 — Register on BLS (if you haven't)

1. Go to **[uk.blsspainglobal.com](https://uk.blsspainglobal.com/Global/account/RegisterUser)**
2. Create an account with your email and password
3. Remember your login credentials — you'll need them in Step 4

### Step 3 — Fork or Upload to GitHub

1. Fork this repo **or** create a new private repository
2. Upload all files including the `.github/` folder

### Step 4 — Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Value |
|--------|-------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID (numbers only) |
| `BLS_EMAIL` | Your BLS login email |
| `BLS_PASSWORD` | Your BLS login password |

### Step 5 — Enable & Test

1. Click the **Actions** tab in your repository
2. Select **BLS Spain Slot Checker** → click **Run workflow**
3. Within 1–2 minutes, check the workflow logs and downloaded screenshots to verify it's working

---

## 📁 Project Structure

```
bls-checker/
├── checker.py                 # Core detection script (Playwright)
├── requirements.txt           # Python dependencies
├── .github/
│   └── workflows/
│       └── checker.yml        # GitHub Actions schedule (every 5 min)
├── screenshots/               # Auto-generated debug screenshots
└── README.md
```

---

## ⚙️ How It Works

```
1. Launch headless Chromium browser
2. Navigate to BLS login page
3. Fill in email + password → Log in
4. Navigate to London Tourist Visit booking page
5. Check for available dates in the calendar
6. If slots found → Send Telegram alert + screenshot
7. If no slots → Log result, wait for next run
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
| GitHub Actions | 2,000 min/month free · this bot uses ~2,000 min/month |
| Telegram Bot API | Free, no limits |
| Playwright | Free, open-source |

---

## 🔧 Run Locally

```bash
# Clone the repo
git clone https://github.com/your-username/bls-checker.git
cd bls-checker

# Install dependencies
pip install -r requirements.txt
playwright install --with-deps chromium

# Set your credentials
export TELEGRAM_BOT_TOKEN="your-token"
export TELEGRAM_CHAT_ID="your-chat-id"
export BLS_EMAIL="your-email"
export BLS_PASSWORD="your-password"

# Run once
python checker.py
```

---

## 🐛 Debugging

Each run generates screenshots saved as GitHub Actions artifacts:

| Screenshot | Description |
|-----------|-------------|
| `01_login_page.png` | Login page loaded |
| `02_login_filled.png` | Email & password filled |
| `03_after_login.png` | State after login attempt |
| `04_visa_type_page.png` | Tourist visa page |
| `05_booking_page.png` | Booking calendar page |
| `06_final_state.png` | Final state when checking slots |
| `error_*.png` | Error states (if any) |

To view: Go to **Actions** → click a workflow run → scroll to **Artifacts** → download `bls-screenshots-*`

---

## ⚠️ Disclaimer

- This tool is for **personal use only**. Do not run at abusive frequencies.
- When a slot is detected, you must **complete the booking manually** — the bot only checks and notifies.
- Using automation may violate BLS Terms of Service. Use at your own risk.

---

## 🤝 Contributing

PRs welcome! Some ideas for future improvements:

- [ ] Support for multiple visa types simultaneously
- [ ] Support for multiple locations (Manchester, Edinburgh)
- [ ] Discord / WeChat notification options
- [ ] Rate limiting / cool-down after successful detection
- [ ] Docker deployment support

---

<div align="center">

Made with ☕ for everyone struggling to get a Spain visa appointment in London.

**If this saved you time, consider giving it a ⭐**

</div>
