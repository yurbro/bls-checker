# 🇪🇸 BLS Spain UK — Visa Slot Checker Bot

自动每 5 分钟检测伦敦 BLS 西班牙签证预约空位，发现 slot 立刻 Telegram 通知。

---

## 📁 项目结构

```
bls-checker/
├── checker.py                    # 主检测脚本
├── requirements.txt              # Python 依赖
├── .github/
│   └── workflows/
│       └── checker.yml           # GitHub Actions 自动运行配置
└── README.md
```

---

## 🚀 部署步骤（约 10 分钟）

### 第一步：创建 Telegram Bot

1. 打开 Telegram，搜索 **@BotFather**
2. 发送 `/newbot`，按提示命名你的 bot
3. 保存返回的 **Bot Token**（格式：`123456789:AABBcc...`）
4. 搜索并打开你刚创建的 bot，发送任意消息（如 `/start`）
5. 打开以下链接获取你的 **Chat ID**（替换 `<TOKEN>`）：
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
   在返回的 JSON 中找到 `"id"` 字段，即为你的 Chat ID

---

### 第二步：上传代码到 GitHub

1. 登录 [github.com](https://github.com)，新建一个 **私有仓库**（建议设为 Private）
2. 将本项目所有文件上传到仓库（包括 `.github` 文件夹）

---

### 第三步：配置 GitHub Secrets

在仓库页面进入：**Settings → Secrets and variables → Actions → New repository secret**

添加以下两个 Secret：

| Secret 名称         | 值                         |
|---------------------|----------------------------|
| `TELEGRAM_BOT_TOKEN` | 你的 Bot Token             |
| `TELEGRAM_CHAT_ID`   | 你的 Chat ID（数字）        |

---

### 第四步：激活 Actions

1. 点击仓库的 **Actions** 标签
2. 如果提示「Workflows aren't running」，点击 **Enable workflows**
3. 手动触发一次测试：点击 `BLS Spain Slot Checker` → **Run workflow**
4. 检查运行日志，并确认 Telegram 收到启动通知

---

## ⚙️ 自定义配置

### 修改检测 URL

打开 `checker.py`，修改第 20 行：
```python
TARGET_URL = "https://blsspainuk.com/appointment/"
```
如果 BLS 实际预约页面 URL 不同，请替换为正确地址。

### 调整关键词

如果检测不准确，可以修改第 23-27 行的关键词：
```python
SLOT_KEYWORDS    = ["available", "select", "choose", "book"]
NO_SLOT_KEYWORDS = ["no appointment", "no slot", "fully booked"]
```

### 修改检测频率

修改 `checker.yml` 中的 cron 表达式：
```yaml
- cron: "*/5 * * * *"   # 每 5 分钟（最小值）
- cron: "*/10 * * * *"  # 每 10 分钟
```

---

## 💰 费用说明

- **GitHub Actions**：公开/私有仓库每月 **2000 分钟免费**
  - 每次运行约 30-60 秒
  - 每 5 分钟一次 = 每月约 1440 次 × 1 分钟 ≈ **1440 分钟/月**
  - 基本刚好在免费额度内 ✅
- **Telegram Bot**：完全免费

---

## 🔧 本地测试（可选）

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export TELEGRAM_BOT_TOKEN="你的Token"
export TELEGRAM_CHAT_ID="你的ChatID"

# 运行一次
python checker.py

# 持续运行（取消 checker.py 末尾注释）
python checker.py
```

---

## ⚠️ 注意事项

- 请勿滥用，过于频繁的请求可能触发 BLS 的反爬机制（5分钟间隔较安全）
- 如果 BLS 页面使用了重定向或登录验证，可能需要升级为 Playwright 方案
- 发现 slot 后请**立刻手动完成预约**，bot 不会自动帮你填表
