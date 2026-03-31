# 🇪🇸 BLS Spain UK — Visa Appointment Slot Checker

Automatically monitors the BLS Spain UK appointment page every 5 minutes and sends an instant Telegram notification when a slot becomes available.

---

## 📁 Project Structure

```
bls-checker/
├── checker.py                    # Main detection script
├── requirements.txt              # Python dependencies
├── .github/
│   └── workflows/
│       └── checker.yml           # GitHub Actions schedule config
└── README.md
```

---

## 🚀 Setup Guide (~10 minutes)

### Step 1: Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` and follow the prompts to name your bot
3. Save the **Bot Token** returned (format: `123456789:AABBcc...`)
4. Search for your newly created bot and send it any message (e.g. `/start`)
5. Open the following URL in your browser to get your **Chat ID** (replace `<TOKEN>`):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
   Find the `"id"` field in the returned JSON — that is your Chat ID

---

### Step 2: Upload Code to GitHub

1. Log in to [github.com](https://github.com) and create a new **private repository**
2. Upload all project files to the repository, including the `.github` folder

---

### Step 3: Configure GitHub Secrets

Go to: **Settings → Secrets and variables → Actions → New repository secret**

Add the following two secrets:

| Secret Name           | Value                        |
|-----------------------|------------------------------|
| `TELEGRAM_BOT_TOKEN`  | Your Bot Token               |
| `TELEGRAM_CHAT_ID`    | Your Chat ID (numbers only)  |

---

### Step 4: Enable GitHub Actions

1. Click the **Actions** tab in your repository
2. If prompted with "Workflows aren't running", click **Enable workflows**
3. Trigger a manual test run: click `BLS Spain Slot Checker` → **Run workflow**
4. Check the run logs and confirm you receive a startup message on Telegram

---

## ⚙️ Configuration

### Change the Target URL

Open `checker.py` and update line 20:
```python
TARGET_URL = "https://blsspainuk.com/appointment/"
```
Replace with the actual booking page URL if it differs.

### Adjust Detection Keywords

If detection results seem inaccurate, update the keywords on lines 23–27:
```python
SLOT_KEYWORDS    = ["available", "select", "choose", "book"]
NO_SLOT_KEYWORDS = ["no appointment", "no slot", "fully booked"]
```

### Change Check Frequency

Edit the cron expression in `checker.yml`:
```yaml
- cron: "*/5 * * * *"    # Every 5 minutes (minimum interval)
- cron: "*/10 * * * *"   # Every 10 minutes
```

---

## 💰 Cost

- **GitHub Actions**: 2,000 free minutes per month for all repositories
  - Each run takes ~30–60 seconds
  - Every 5 minutes = ~1,440 runs/month × 1 minute ≈ **1,440 minutes/month**
  - Stays comfortably within the free tier ✅
- **Telegram Bot**: Completely free

---

## 🔧 Local Testing (Optional)

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_BOT_TOKEN="your-token-here"
export TELEGRAM_CHAT_ID="your-chat-id-here"

# Run once
python checker.py

# Run continuously (uncomment the loop at the bottom of checker.py)
python checker.py
```

---

## ⚠️ Important Notes

- Do not abuse the checker — requests every 5 minutes are safe and unlikely to trigger rate limiting
- If the BLS page requires a login or uses heavy JavaScript rendering, the script may need to be upgraded to use Playwright
- When a slot is detected, **you must complete the booking manually** — the bot will not fill in forms or submit on your behalf
