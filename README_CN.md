<div align="center">

# 🇪🇸 BLS Spain UK — 签证预约抢位机器人

**再也不用手动刷新预约页面了。**

每 5 分钟自动监测 BLS 西班牙签证（伦敦）预约页面，一旦有空位立刻发送 Telegram 通知。

🌐 [English](./README.md) | [中文](./README_CN.md)

---

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-免费-2088FF?style=flat-square&logo=github-actions&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=flat-square&logo=telegram&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## ✨ 功能特点

- 🔍 **自动检测** BLS Spain UK 预约页面的可用时间段
- 📲 **即时 Telegram 推送** — 有空位立刻通知你，抢在别人前面
- ⏱️ **每 5 分钟运行一次** — 基于 GitHub Actions，完全免费
- 🛡️ **优雅的错误处理** — 超时、被拦截、网络波动都不会导致崩溃
- 🔒 **零信息泄露** — 所有密钥通过 GitHub Secrets 管理，不写死在代码里

---

## 🚀 部署步骤

### 第一步 — 创建 Telegram Bot

1. 打开 Telegram，搜索 **[@BotFather](https://t.me/BotFather)**
2. 发送 `/newbot`，按提示为 bot 取名
3. 复制返回的 **Bot Token**，格式类似 `123456789:AABBccDDee...`
4. 找到你的新 bot，发送任意消息（如 `/start`）
5. 在浏览器中打开以下链接获取 **Chat ID**（替换 `<YOUR_TOKEN>`）：
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
   在返回的 JSON 里找到 `"id"` 字段，即为你的 Chat ID

### 第二步 — 上传代码到 GitHub

1. Fork 本仓库，**或者**新建一个私有仓库
2. 上传全部文件，包括 `.github/` 文件夹

### 第三步 — 配置 GitHub Secrets

进入仓库：**Settings → Secrets and variables → Actions → New repository secret**

| Secret 名称 | 填入内容 |
|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | 你的 Bot Token |
| `TELEGRAM_CHAT_ID` | 你的 Chat ID（纯数字） |

### 第四步 — 启用并测试

1. 点击仓库顶部 **Actions** 标签
2. 选择 **BLS Spain Slot Checker** → 点击 **Run workflow**
3. 约 30 秒后，Telegram 收到启动通知即代表成功 ✅

---

## 📁 项目结构

```
bls-checker/
├── checker.py                 # 核心检测脚本
├── requirements.txt           # Python 依赖
├── .github/
│   └── workflows/
│       └── checker.yml        # GitHub Actions 定时配置（每 5 分钟）
└── README.md
```

---

## ⚙️ 自定义配置

所有配置都在 `checker.py` 顶部：

```python
# 目标 URL — 如果 BLS 更换了预约页面地址，在这里修改
TARGET_URL = "https://blsspainuk.com/appointment/"

# 出现以下任意关键词 → 判定为有空位
SLOT_KEYWORDS = ["available", "select", "choose", "book", "confirm"]

# 出现以下任意关键词 → 判定为无空位
NO_SLOT_KEYWORDS = ["no appointment", "no slot", "fully booked", "unavailable"]
```

### 修改检测频率

编辑 `.github/workflows/checker.yml` 里的 cron 表达式：

```yaml
- cron: "*/5 * * * *"    # 每 5 分钟（推荐，也是最小间隔）
- cron: "*/10 * * * *"   # 每 10 分钟
```

---

## 💰 完全免费

| 服务 | 费用 |
|------|------|
| GitHub Actions | 每月 2000 分钟免费 · 本 bot 月均消耗约 1440 分钟 |
| Telegram Bot API | 完全免费，无任何限制 |

---

## 🔧 本地运行（可选）

```bash
# 克隆仓库
git clone https://github.com/your-username/bls-checker.git
cd bls-checker

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export TELEGRAM_BOT_TOKEN="你的Token"
export TELEGRAM_CHAT_ID="你的ChatID"

# 运行一次
python checker.py
```

如需持续运行，取消 `checker.py` 末尾 `while True` 循环的注释即可。

---

## ⚠️ 注意事项

- 本工具仅供**个人合理使用**，请勿频繁请求导致对方服务器压力
- 检测到空位后，**需要你手动完成预约**，bot 不会自动填表或提交
- 如果 BLS 网站加入了登录验证或重度 JS 渲染，可能需要升级为 [Playwright](https://playwright.dev/) 方案

---

## 🤝 欢迎贡献

欢迎提 PR！以下是一些待实现的功能：

- [ ] Playwright 支持（应对 JS 渲染页面）
- [ ] 支持多个预约类型同时监测
- [ ] 企业微信 / Server酱通知支持
- [ ] Docker 一键部署

---

<div align="center">

为所有在伦敦苦苦抢西班牙签证预约的人而做 ☕

**如果这个项目帮到了你，欢迎点一个 ⭐**

</div>
