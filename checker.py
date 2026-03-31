"""
BLS Spain UK — Appointment Slot Checker (Playwright 版)
使用无头浏览器登录 BLS 系统，检测 London Tourist Visit 是否有可用预约时间。
发现空位立刻通过 Telegram 通知。

所有敏感信息通过环境变量读取，绝不硬编码。
"""

import asyncio
import os
import sys
import requests
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# ─────────────────────────────────────────────
# 配置区（全部从环境变量读取）
# ─────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID",   "")
BLS_EMAIL          = os.environ.get("BLS_EMAIL",          "")
BLS_PASSWORD       = os.environ.get("BLS_PASSWORD",       "")

# BLS 系统 URL
LOGIN_URL       = "https://uk.blsspainglobal.com/Global/account/login"
APPOINTMENT_URL = "https://uk.blsspainglobal.com/Global/blsappointment/manageappointment"
VISA_TYPE_URL   = "https://uk.blsspainglobal.com/Global/bls/visatypeverification"

# London Tourist Visit 对应的预约页面
BOOK_URL = "https://uk.blsspainglobal.com/Global/bls/AllVisaType?VisaTypeCode=TOURIST_VISA"

# 截图保存路径（GitHub Actions 中可通过 artifact 上传）
SCREENSHOT_DIR = os.environ.get("SCREENSHOT_DIR", "screenshots")

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
        "disable_web_page_preview": True,
    }
    try:
        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()
        print(f"[Telegram] 消息发送成功 ✓")
        return True
    except Exception as e:
        print(f"[Telegram] 发送失败: {e}")
        return False


def send_telegram_photo(photo_path: str, caption: str = "") -> bool:
    """发送截图到 Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    try:
        with open(photo_path, "rb") as f:
            resp = requests.post(
                url,
                data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption, "parse_mode": "HTML"},
                files={"photo": f},
                timeout=30,
            )
        resp.raise_for_status()
        print(f"[Telegram] 截图发送成功 ✓")
        return True
    except Exception as e:
        print(f"[Telegram] 截图发送失败: {e}")
        return False


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────
def ensure_screenshot_dir():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)


async def save_screenshot(page, name: str) -> str:
    """保存截图并返回路径"""
    ensure_screenshot_dir()
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    await page.screenshot(path=path, full_page=True)
    print(f"[截图] 已保存: {path}")
    return path


# ─────────────────────────────────────────────
# 核心逻辑
# ─────────────────────────────────────────────
async def login(page) -> bool:
    """
    登录 BLS 系统。
    返回 True 表示登录成功。
    """
    print(f"[步骤 1] 导航到登录页面: {LOGIN_URL}")
    try:
        await page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=30000)
    except PlaywrightTimeout:
        print("[错误] 登录页面加载超时")
        await save_screenshot(page, "error_login_timeout")
        return False

    # 等待页面完全加载
    await page.wait_for_timeout(2000)
    await save_screenshot(page, "01_login_page")

    # 检查是否网站宕机
    page_text = await page.inner_text("body")
    if "temporarily unavailable" in page_text.lower() or "application error" in page_text.lower():
        print("[错误] 网站暂时不可用 (Application Temporarily Unavailable)")
        send_telegram("⚠️ BLS 网站暂时不可用，等待下次检测。")
        return False

    # 填写登录表单
    print("[步骤 2] 填写登录信息...")
    try:
        # 查找邮箱输入框（多种选择器兼容）
        email_input = page.locator('input[name="UserId"], input[id="UserId"], input[type="email"], input[placeholder*="mail" i], input[placeholder*="user" i]').first
        await email_input.wait_for(state="visible", timeout=10000)
        await email_input.fill(BLS_EMAIL)

        # 查找密码输入框
        pwd_input = page.locator('input[name="Password"], input[id="Password"], input[type="password"]').first
        await pwd_input.wait_for(state="visible", timeout=5000)
        await pwd_input.fill(BLS_PASSWORD)

        await save_screenshot(page, "02_login_filled")

        # 点击登录按钮
        login_btn = page.locator('button[type="submit"], input[type="submit"], button:has-text("Login"), button:has-text("Sign in"), a:has-text("Login")').first
        await login_btn.click()

        # 等待页面导航
        print("[步骤 3] 等待登录响应...")
        await page.wait_for_load_state("domcontentloaded", timeout=20000)
        await page.wait_for_timeout(3000)
        await save_screenshot(page, "03_after_login")

    except PlaywrightTimeout:
        print("[错误] 登录表单元素未找到或操作超时")
        await save_screenshot(page, "error_login_form")
        return False
    except Exception as e:
        print(f"[错误] 登录过程异常: {e}")
        await save_screenshot(page, "error_login_exception")
        return False

    # 检查是否登录成功
    current_url = page.url
    page_text = await page.inner_text("body")

    # 如果还在登录页面，检查是否有错误消息
    if "login" in current_url.lower() and "account/login" in current_url.lower():
        if "invalid" in page_text.lower() or "incorrect" in page_text.lower() or "error" in page_text.lower():
            print("[错误] 登录失败：用户名或密码错误")
            send_telegram("❌ BLS 登录失败：用户名或密码错误，请检查 GitHub Secrets 设置。")
            return False

    print(f"[成功] 登录后页面: {current_url}")
    return True


async def navigate_to_appointment(page) -> bool:
    """
    登录后导航到预约页面（London Tourist Visit）。
    返回 True 表示已到达目标页面。
    """
    print("[步骤 4] 导航到预约页面...")

    try:
        # 方法 1: 直接访问 London Tourist Visit 预约页面
        await page.goto(BOOK_URL, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        await save_screenshot(page, "04_visa_type_page")

        page_text = await page.inner_text("body")
        current_url = page.url

        # 如果被重定向到登录页面，说明 session 失效
        if "account/login" in current_url.lower():
            print("[错误] 被重定向回登录页面，session 可能已失效")
            return False

        # 检查页面是否正常加载
        if "temporarily unavailable" in page_text.lower():
            print("[错误] 网站暂时不可用")
            return False

        print(f"[成功] 已到达页面: {current_url}")

        # 方法 2: 尝试点击 "Book New Appointment" 链接
        try:
            book_link = page.locator('a:has-text("Book New Appointment"), a:has-text("Book Appointment"), a[href*="visatypeverification"], a[href*="manageappointment"]').first
            if await book_link.is_visible():
                await book_link.click()
                await page.wait_for_load_state("domcontentloaded", timeout=15000)
                await page.wait_for_timeout(3000)
                await save_screenshot(page, "05_booking_page")
                print(f"[导航] 点击预约链接后: {page.url}")
        except Exception:
            # 如果链接不存在，继续在当前页面检测
            pass

        return True

    except PlaywrightTimeout:
        print("[错误] 预约页面加载超时")
        await save_screenshot(page, "error_appointment_timeout")
        return False
    except Exception as e:
        print(f"[错误] 导航异常: {e}")
        await save_screenshot(page, "error_navigation")
        return False


async def check_slot_availability(page) -> tuple[bool, str]:
    """
    检查当前页面是否有可用的预约 slot。
    
    检测策略（多层次）：
    1. 查找日历组件中可点击的日期
    2. 查找 "Book Appointment" 按钮/链接是否可用
    3. 检查页面文字是否包含明确的 "没有 slot" 提示
    4. 查找 datepicker / calendar 元素
    
    返回 (是否有slot, 详细描述)
    """
    print("[步骤 5] 检测 slot 可用性...")

    page_text = (await page.inner_text("body")).lower()
    current_url = page.url

    # ---- 检查明确的 "没有 slot" 信号 ----
    no_slot_signals = [
        "no appointment slots are currently available",
        "no slots are currently available",
        "no available slot",
        "no dates are available",
        "currently no dates available",
        "slot is not available",
        "fully booked",
        "no appointment is available",
        "sorry, no dates",
        "no slots available",
        "there are no available dates",
        "appointment dates are not available",
    ]

    for signal in no_slot_signals:
        if signal in page_text:
            return False, f"页面明确显示: '{signal}'"

    # ---- 检查日历组件 ----
    # BLS 通常使用 jQuery UI datepicker 或类似日历
    calendar_selectors = [
        ".ui-datepicker td a",              # jQuery UI datepicker 可选日期
        ".datepicker td:not(.disabled)",     # Bootstrap datepicker
        ".calendar td.available",
        "td.day:not(.disabled):not(.off)",   # 日历可用日期
        ".fc-day:not(.fc-day-disabled)",     # FullCalendar
        "input[type='date']",
        ".appointment-calendar td a",
        "[data-date]",                       # 带 data-date 属性的元素
    ]

    for selector in calendar_selectors:
        try:
            elements = await page.locator(selector).all()
            if elements:
                count = len(elements)
                print(f"[发现] 找到 {count} 个可选日期元素 (选择器: {selector})")

                # 尝试获取日期文本
                dates_text = []
                for el in elements[:5]:  # 最多取前5个
                    try:
                        text = await el.inner_text()
                        if text.strip():
                            dates_text.append(text.strip())
                    except Exception:
                        pass

                detail = f"找到 {count} 个可选日期"
                if dates_text:
                    detail += f"（如: {', '.join(dates_text)}）"
                return True, detail
        except Exception:
            continue

    # ---- 检查可见的日期选择器 ----
    try:
        date_inputs = await page.locator('input[id*="date" i], input[name*="date" i], input[id*="appointment" i]').all()
        for inp in date_inputs:
            if await inp.is_visible() and await inp.is_enabled():
                placeholder = await inp.get_attribute("placeholder") or ""
                if "select" in placeholder.lower() or "date" in placeholder.lower() or placeholder == "":
                    return True, f"找到可用的日期输入框 (placeholder: {placeholder})"
    except Exception:
        pass

    # ---- 检查积极信号 ----
    slot_signals = [
        "select your preferred date",
        "select appointment date",
        "choose a date",
        "pick a date",
        "available dates",
        "appointment is available",
        "slots available",
        "select date and time",
        "select an available date",
    ]
    for signal in slot_signals:
        if signal in page_text:
            return True, f"页面显示积极信号: '{signal}'"

    # ---- 检查是否在申请人数量选择页面 (也表示有 slot) ----
    applicant_signals = [
        "number of applicant",
        "how many applicant",
        "select number of",
        "no. of applicant",
    ]
    for signal in applicant_signals:
        if signal in page_text:
            return True, f"页面要求选择申请人数（说明有预约可用）: '{signal}'"

    # ---- 无法判断 ----
    # 截取页面关键区域的文字供调试
    preview = page_text[:500].replace('\n', ' ').strip()
    return False, f"未能明确判断（可能页面结构变了或暂无 slot）。URL: {current_url}\n页面预览: {preview}"


async def run_checker():
    """主检测流程"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'═' * 60}")
    print(f"  BLS Spain UK - Slot Checker (Playwright)")
    print(f"  检测时间: {now}")
    print(f"  目标: London → Tourist Visit")
    print(f"{'═' * 60}\n")

    # 检查必要的环境变量
    if not BLS_EMAIL or not BLS_PASSWORD:
        print("[致命错误] 未设置 BLS_EMAIL 或 BLS_PASSWORD 环境变量")
        print("请在 GitHub Secrets 中添加 BLS_EMAIL 和 BLS_PASSWORD")
        send_telegram("❌ BLS Checker 配置错误：缺少 BLS_EMAIL 或 BLS_PASSWORD")
        sys.exit(1)

    async with async_playwright() as p:
        # 启动浏览器（无头模式）
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
            ],
        )

        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
            locale="en-GB",
        )

        # 禁用 webdriver 检测
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        page = await context.new_page()

        try:
            # Step 1-3: 登录
            if not await login(page):
                print("[终止] 登录失败，退出检测")
                await browser.close()
                return

            # Step 4: 导航到预约页面
            if not await navigate_to_appointment(page):
                print("[终止] 无法到达预约页面，退出检测")
                await browser.close()
                return

            # Step 5: 检测 slot
            found, detail = await check_slot_availability(page)
            screenshot_path = await save_screenshot(page, "06_final_state")

            if found:
                print(f"\n🎉🎉🎉 发现可用 SLOT！🎉🎉🎉")
                print(f"详情: {detail}")
                msg = (
                    "🚨🚨🚨 <b>BLS 西班牙签证 London Tourist Visit — 发现可用预约！</b>\n\n"
                    f"📋 详情: {detail}\n\n"
                    f"🔗 <a href='{LOGIN_URL}'>立即登录预约</a>\n\n"
                    f"🕐 检测时间: {now}\n\n"
                    "⚡ <b>请立即前往预约！slot 可能随时被抢！</b>"
                )
                send_telegram(msg)
                # 同时发送截图
                send_telegram_photo(screenshot_path, "📸 预约页面截图")
            else:
                print(f"\n[暂无 slot] {detail}")
                # 不发 Telegram（避免刷屏），仅打印日志

        except Exception as e:
            print(f"[未知错误] {e}")
            try:
                await save_screenshot(page, "error_unknown")
            except Exception:
                pass
            send_telegram(f"⚠️ BLS Checker 运行异常: {str(e)[:200]}")
        finally:
            await browser.close()

    print(f"\n[完成] 检测结束 @ {datetime.now().strftime('%H:%M:%S')}")


def main():
    # 发送启动通知（仅在有 Telegram 配置时）
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        send_telegram(
            f"🤖 <b>BLS Slot Checker 已启动</b>\n"
            f"📍 London → Tourist Visit\n"
            f"🔍 正在检测...\n"
            f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

    asyncio.run(run_checker())


if __name__ == "__main__":
    main()
