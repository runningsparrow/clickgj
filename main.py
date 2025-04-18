# project_root/
# ├── main.py             # 主入口文件
# ├── config/
# │   ├── __init__.py
# │   ├── settings.py     # 所有配置项
# │   └── selectors.py    # 页面元素选择器
# └── utils/
#     ├── __init__.py
#     └── browser.py      # 浏览器工具类

# 关键设计特点
#
#     严格的分层架构：配置、工具和业务逻辑分离
#
#     完善的错误处理：自动截图+日志记录关键操作
#
#     跨平台兼容：路径处理使用pathlib，自动识别操作系统
#
#     可维护性：所有选择器集中管理，修改方便
#
#     可扩展性：通过装饰器实现重试机制等高级功能
#
#     生产就绪：完整的日志系统和资源清理机制

import logging
from playwright.sync_api import sync_playwright
from config.settings import BASE_URL, TIMEOUT
from config.selectors import LOGIN, DASHBOARD
from utils.browser import BrowserUtils, PageUtils


def main():
    with sync_playwright() as p:
        try:
            # 动态覆盖配置
            custom_config = {
                # "channel": "firefox",  # 使用Firefox
                "headless": False  # 可见模式
            }
            # 初始化浏览器
            browser, context, page = BrowserUtils.launch_browser(p)
            browser_utils = BrowserUtils(page)

            # 访问目标网站
            browser_utils.navigate(BASE_URL)

            # 执行登录操作 (示例)
            page.fill(LOGIN["username"], "admin")
            page.fill(LOGIN["password"], "password123")
            browser_utils.click_element(LOGIN["submit_button"])

            # 验证登录成功
            page.wait_for_selector(DASHBOARD["welcome_message"], timeout=TIMEOUT * 1000)

            # 使用重试装饰器的示例
            @PageUtils.retry_operation(max_retries=3, delay=2.0)
            def sensitive_operation():
                browser_utils.click_element(DASHBOARD["menu_item"]("Reports"))
                assert "Report Dashboard" in page.title()

            sensitive_operation()

            # 捕获最终截图
            browser_utils.capture_screenshot("final_page")

        except Exception as e:
            logging.error(f"执行失败: {str(e)}", exc_info=True)
            if 'browser_utils' in locals():
                browser_utils.capture_screenshot("error_final")
            raise
        finally:
            # 确保资源释放
            if 'browser' in locals():
                browser.close()
            logging.info("自动化流程执行结束")


if __name__ == "__main__":
    main()
