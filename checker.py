"""
BLS Spain UK - Appointment Slot Checker
自动检测 BLS 西班牙签证预约 slot，发现空位立刻 Telegram 通知
"""

import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ─────────────────────────────────────────────
# 配置区（本地测试时可直接填写，正式部署用环境变量）
# ─────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID",   "")

# BLS 预约页面（如果跳转请更换为实际 URL）
TARGET_URL = "https://blsspainuk.com/appointment/"

# 检测关键词：出现以下任意词 → 有 slot；如果只看到 NO_SLOT_KEYWORDS → 没有
SLOT_KEYWORDS    = ["available", "select", "choose", "book", "confirm", "时间段", "可用"]
NO_SLOT_KEYWORDS = ["no appointment", "no slot", "currently unavailable",
                    "no available", "no dates", "fully booked"]

# 模拟真实浏览器 headers，降低被拦截概率
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-GB,en;q=0.9,zh-CN;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://blsspainuk.com/",
    "Connection": "keep-alive",
}

# ─────────────────────────────────────────────
# Telegram 通知
# ─────────────────────────────────────────────
def send_telegram(message: str) -> bool:
    """发送 Telegram 消息，返回是否成功"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[警告] 未设置 Telegram Token 或 Chat ID，跳过通知")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        print(f"[Telegram] 消息发送成功 ✓")
        return True
    except Exception as e:
        print(f"[Telegram] 发送失败: {e}")
        return False

# ─────────────────────────────────────────────
# 页面抓取 & 检测
# ─────────────────────────────────────────────
def fetch_page(url: str, session: requests.Session) -> str | None:
    """抓取页面，返回 HTML 文本，失败返回 None"""
    try:
        resp = session.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        return resp.text
    except requests.exceptions.HTTPError as e:
        print(f"[错误] HTTP 错误 {e.response.status_code}: {url}")
    except requests.exceptions.ConnectionError:
        print(f"[错误] 无法连接: {url}")
    except requests.exceptions.Timeout:
        print(f"[错误] 请求超时: {url}")
    except Exception as e:
        print(f"[错误] 未知错误: {e}")
    return None


def has_slot(html: str) -> tuple[bool, str]:
    """
    解析 HTML，判断是否有可用 slot。
    返回 (是否有slot, 页面摘要文字)
    """
    soup = BeautifulSoup(html, "html.parser")

    # 提取正文可见文字（去掉 script/style）
    for tag in soup(["script", "style", "noscript", "meta"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True).lower()

    # 1. 如果明确看到「没有 slot」关键词 → 没有
    for kw in NO_SLOT_KEYWORDS:
        if kw.lower() in text:
            return False, f'页面含「{kw}」，暂无空位'

    # 2. 如果看到「有 slot」关键词 → 有！
    for kw in SLOT_KEYWORDS:
        if kw.lower() in text:
            # 截取关键词周围 200 字符作为摘要
            idx = text.find(kw.lower())
            snippet = text[max(0, idx-80): idx+120].strip()
            return True, snippet

    # 3. 都没匹配到：可能页面结构变了，保守返回 False 并打印原始文字供调试
    preview = text[:300]
    return False, f'未能识别页面内容（可能需要调整关键词）: {preview}'


# ─────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────
def check_once(session: requests.Session) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'─'*50}")
    print(f"[{now}] 开始检测: {TARGET_URL}")

    html = fetch_page(TARGET_URL, session)
    if html is None:
        print("[跳过] 页面抓取失败，等待下次检测")
        return

    found, detail = has_slot(html)

    if found:
        print(f"🎉 发现可用 SLOT！")
        msg = (
            "🚨 <b>BLS 西班牙签证 London — 发现可用预约时间！</b>\n\n"
            f"🔗 <a href='{TARGET_URL}'>立即前往预约</a>\n\n"
            f"📝 页面摘要:\n<code>{detail[:300]}</code>\n\n"
            f"🕐 检测时间: {now}"
        )
        send_telegram(msg)
    else:
        print(f"[暂无 slot] {detail[:120]}")


def main():
    session = requests.Session()
    # 发送启动通知（可选）
    send_telegram(
        f"🤖 <b>BLS Slot Checker 已启动</b>\n"
        f"监测地址: {TARGET_URL}\n"
        f"发现空位将立即通知你 ✅"
    )

    # 如果在 GitHub Actions 中运行（单次执行）
    check_once(session)

    # 如果在本地持续运行，取消下方注释（每3分钟检测一次）
    # while True:
    #     check_once(session)
    #     print(f"[等待] 3 分钟后再次检测...")
    #     time.sleep(180)


if __name__ == "__main__":
    main()
