import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from playwright.sync_api import Page, BrowserContext, Browser
from config.settings import BROWSER_CONFIG, LOG_DIR, SCREENSHOT_DIR, TIMEOUT


class BrowserUtils:
    """浏览器操作工具类"""

    def __init__(self, page: Page):
        self.page = page
        self._setup_logging()

    def _setup_logging(self):
        """配置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOG_DIR / 'browser_ops.log'),
                logging.StreamHandler()
            ]
        )

    # @classmethod
    # def launch_browser(cls, playwright) -> Tuple[Browser, BrowserContext, Page]:
    #     """启动浏览器并返回实例三元组"""
    #     browser = playwright.chromium.launch(**BROWSER_CONFIG)
    #     context = browser.new_context()
    #     page = context.new_page()
    #     return browser, context, page

    @classmethod
    def launch_browser(cls, playwright, custom_config=None):
        # 合并默认配置和自定义配置
        config = {**BROWSER_CONFIG, **(custom_config or {})}
        browser = playwright.chromium.launch(**config)
        context = browser.new_context()
        page = context.new_page()
        return browser, context, page

    def navigate(self, url: str, timeout: float = TIMEOUT):
        """带错误处理的页面跳转"""
        try:
            self.page.goto(url, timeout=timeout * 1000)
            logging.info(f"成功导航至: {url}")
        except Exception as e:
            self.capture_screenshot("navigation_error")
            raise Exception(f"导航失败: {url} - {str(e)}")

    def capture_screenshot(self, name: str, full_page: bool = True) -> Path:
        """捕获截图并返回文件路径"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = SCREENSHOT_DIR / f"{name}_{timestamp}.png"
        self.page.screenshot(path=str(screenshot_path), full_page=full_page)
        logging.info(f"截图已保存: {screenshot_path}")
        return screenshot_path

    def save_page_content(self, name: str) -> Path:
        """保存页面HTML内容"""
        html_path = LOG_DIR / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        html_path.write_text(self.page.content(), encoding="utf-8")
        return html_path

    def click_element(self, selector: str, timeout: float = TIMEOUT):
        """带自动等待的点击操作"""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout * 1000)
            self.page.click(selector)
            logging.info(f"成功点击元素: {selector}")
        except Exception as e:
            self.capture_screenshot("click_error")
            raise Exception(f"点击元素失败: {selector} - {str(e)}")

    def wait_for_network_idle(self, timeout: float = TIMEOUT):
        """等待网络空闲"""
        self.page.wait_for_load_state("networkidle", timeout=timeout * 1000)


class PageUtils:
    """页面操作工具类"""

    @staticmethod
    def retry_operation(max_retries: int = 3, delay: float = 1.0):
        """操作重试装饰器"""

        def decorator(func):
            def wrapper(*args, **kwargs):
                last_exception = None
                for attempt in range(1, max_retries + 1):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        if attempt < max_retries:
                            logging.warning(f"尝试 {attempt}/{max_retries} 失败，等待重试...")
                            time.sleep(delay)
                raise last_exception

            return wrapper

        return decorator
