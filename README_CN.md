<div align="center">

# 🇪🇸 BLS 西班牙签证（英国）— 预约空位检测器

**再也不会错过签证预约了。**

使用真实浏览器（Playwright）登录 BLS 系统，检测 London Tourist Visit 预约日历，一有空位立即 Telegram 通知你。

🌐 [English](./README.md) | [中文](./README_CN.md)

---

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-无头浏览器-2EAD33?style=flat-square&logo=playwright&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-免费-2088FF?style=flat-square&logo=github-actions&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-机器人通知-26A5E4?style=flat-square&logo=telegram&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## ✨ 功能特点

- 🌐 **真实浏览器自动化** — 使用 Playwright（无头 Chromium）处理登录、JS渲染和动态内容
- 🔐 **自动登录 BLS 账号** — 模拟完整的预约流程来检测可用日期
- 📲 **发现空位立即 Telegram 通知** 并附带截图
- ⏱️ **每 5 分钟检测一次** — 通过 GitHub Actions 运行，完全免费
- 📸 **调试截图** — 每次运行保存截图，可在 GitHub Actions artifacts 中下载
- 🛡️ **优雅的错误处理** — 网站宕机、登录失败、超时都能妥善处理
- 🔒 **安全** — 所有凭据存储在 GitHub Secrets 中，绝不写入代码

---

## 🚀 快速开始

### 第一步 — 创建 Telegram 机器人

1. 打开 Telegram，搜索 **[@BotFather](https://t.me/BotFather)**
2. 发送 `/newbot` 并按提示操作
3. 复制你的 **Bot Token**（格式如 `123456789:AABBccDDee...`）
4. 向你的新机器人发送 `/start` 开始对话
5. 在浏览器中打开以下 URL 获取你的 **Chat ID**：
   ```
   https://api.telegram.org/bot<你的Token>/getUpdates
   ```
   在返回的 JSON 中找到 `"id"` 字段

### 第二步 — 注册 BLS 账号（如果还没有）

1. 前往 **[uk.blsspainglobal.com](https://uk.blsspainglobal.com/Global/account/RegisterUser)**
2. 用你的邮箱注册账号
3. 记住登录凭据——第四步需要用到

### 第三步 — Fork 或上传到 GitHub

1. Fork 本仓库 **或** 创建一个新的私有仓库
2. 上传所有文件，包括 `.github/` 文件夹

### 第四步 — 添加 GitHub Secrets

进入 **Settings → Secrets and variables → Actions → New repository secret**

| Secret 名称 | 值 |
|-------------|-----|
| `TELEGRAM_BOT_TOKEN` | 你的 Telegram 机器人 Token |
| `TELEGRAM_CHAT_ID` | 你的 Telegram Chat ID（纯数字） |
| `BLS_EMAIL` | 你的 BLS 登录邮箱 |
| `BLS_PASSWORD` | 你的 BLS 登录密码 |

### 第五步 — 启用并测试

1. 点击仓库的 **Actions** 标签
2. 选择 **BLS Spain Slot Checker** → 点击 **Run workflow**
3. 1-2 分钟内，检查 workflow 日志和下载的截图确认是否正常工作

---

## 📁 项目结构

```
bls-checker/
├── checker.py                 # 核心检测脚本（Playwright）
├── requirements.txt           # Python 依赖
├── .github/
│   └── workflows/
│       └── checker.yml        # GitHub Actions 定时任务（每5分钟）
├── screenshots/               # 自动生成的调试截图
└── README.md
```

---

## ⚙️ 工作原理

```
1. 启动无头 Chromium 浏览器
2. 导航到 BLS 登录页面
3. 填写邮箱 + 密码 → 登录
4. 导航到 London Tourist Visit 预约页面
5. 检查日历中是否有可选日期
6. 有空位 → 发送 Telegram 通知 + 截图
7. 无空位 → 记录日志，等待下次检测
```

### 修改检测频率

编辑 `.github/workflows/checker.yml` 中的 cron 表达式：

```yaml
- cron: "*/5 * * * *"    # 每 5 分钟（推荐）
- cron: "*/10 * * * *"   # 每 10 分钟
```

> **注意：** 5 分钟是 GitHub Actions 的最小间隔。

---

## 💰 完全免费

| 服务 | 费用 |
|------|------|
| GitHub Actions | 每月 2,000 分钟免费 · 本项目约使用 2,000 分钟/月 |
| Telegram Bot API | 免费，无限制 |
| Playwright | 免费，开源 |

---

## 🔧 本地运行

```bash
# 克隆仓库
git clone https://github.com/your-username/bls-checker.git
cd bls-checker

# 安装依赖
pip install -r requirements.txt
playwright install --with-deps chromium

# 设置凭据（Windows 用 set 代替 export）
export TELEGRAM_BOT_TOKEN="你的token"
export TELEGRAM_CHAT_ID="你的chatid"
export BLS_EMAIL="你的邮箱"
export BLS_PASSWORD="你的密码"

# 运行一次
python checker.py
```

---

## 🐛 调试

每次运行会生成截图，保存为 GitHub Actions artifacts：

| 截图文件 | 说明 |
|---------|------|
| `01_login_page.png` | 登录页面已加载 |
| `02_login_filled.png` | 已填写邮箱和密码 |
| `03_after_login.png` | 登录后的状态 |
| `04_visa_type_page.png` | Tourist Visit 页面 |
| `05_booking_page.png` | 预约日历页面 |
| `06_final_state.png` | 检测 slot 时的最终状态 |
| `error_*.png` | 错误状态截图（如有） |

查看方法：进入 **Actions** → 点击某次运行 → 滚动到 **Artifacts** → 下载 `bls-screenshots-*`

---

## ⚠️ 免责声明

- 本工具仅供 **个人使用**，请勿以过高频率运行
- 检测到空位后，你需要 **手动完成预约** — 机器人不会自动提交任何表单
- 使用自动化工具可能违反 BLS 服务条款，请自行承担风险

---

<div align="center">

为每一个在伦敦苦苦等待西班牙签证预约的人而做 ☕

**如果这个项目帮到了你，请给个 ⭐**

</div>
