# 初始项目结构
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

# 项目结构调整
# project_root/
# ├── .env                    # 本地开发环境变量
# ├── main.py
# ├── config/
# │   ├── __init__.py
# │   ├── settings.py         # 包含所有配置（含凭证读取逻辑）
# │   ├── credentials.py      # （可选）单独存放凭证相关逻辑
# │   └── selectors.py
# └── utils/
#     ├── __init__.py
#     └── browser.py

import logging
import sys

from playwright.sync_api import sync_playwright
from config.settings import BASE_URL, TIMEOUT, Credentials_user
from config.selectors import get_selector
from utils.browser import BrowserUtils, PageUtils
from config.credentials import SecureCredentials, SecurityError


def main():
    logging.info("获取用户名和密码")
    try:
        # 获取用户
        username = Credentials_user.get_username()

        # 新代码（使用加密方案）
        # username = os.getenv('LOGIN_USER')  # 用户名通常不需要加密
        password = SecureCredentials.get_password()  # 密码从加密存储获取

        # 联合验证
        if not all([username, password]):
            raise SecurityError("凭证不完整")

        Credentials_user.validate()

    except ValueError as e:
        logging.critical(f"配置错误: {e}")
        sys.exit(1)

    except SecurityError as e:
        logging.critical(f"安全错误: {e}")
        sys.exit(1)

    with sync_playwright() as p:
        try:
            print(p.chromium.executable_path)  # 打印Chromium实际路径
            # 动态覆盖配置
            custom_config = {
                # "channel": "firefox",  # 使用Firefox
                "headless": False,  # 可见模式
                # "devtools": True  # 同时打开开发者工具
            }
            # 初始化浏览器
            # browser, context, page = BrowserUtils.launch_browser(p)
            # 修改后的调用方式
            browser, context, page = BrowserUtils.launch_browser(p, custom_config=custom_config)
            browser_utils = BrowserUtils(page)

            # 访问目标网站
            browser_utils.navigate(BASE_URL)

            # ==========================================================================
            # 修改后的点击登录按钮代码
            # 方法1：直接使用page.click()方法
            page.click('a.btn.btn-default:has-text("登录")')

            # 或者方法2：修改为使用选择器字符串
            # browser_utils.click_element('a.btn.btn-default:has-text("登录")')
            print(page.title())
            # print(page.content())
            # ==========================================================================

            # =============

            # 执行登录操作
            # 填写用户名和密码
            # page.fill('input[name="user_name"]', "13918682062")
            # page.fill('input[name="password"]', "1111111")
            page.fill('input[name="user_name"]', username)
            page.fill('input[name="password"]', password)

            print("bug1")

            # 勾选"记住我"复选框（通过name属性定位）
            page.check('input[name="auto_login"]')

            print("bug2")

            # 勾选用户协议复选框 - 最佳方案
            try:
                # 方法1：通过label文本点击（首选）
                page.click('div.user_agree .agree_text')
                print("bug3.1")
            except:
                # 方法2：备用方案 - 直接JS操作
                page.eval_on_selector('div.user_agree > input[type="checkbox"]', 'el => el.click()')
                print("bug3.2")

            print("bug3")

            # 点击登录按钮
            page.click('a.btn.btn-jisilu:has-text("登录")')

            print("bug4")

            # =============

            # 新验证代码：
            inbox_btn = page.wait_for_selector(
                'a#index_btn.btn.btn-default[href="/inbox/"]',
                state="visible",
                timeout=TIMEOUT * 1000
            )
            logging.info("登录成功验证：私信按钮已加载")

            print("bug5")

            # 使用重试装饰器的示例（适配新选择器系统）
            @PageUtils.retry_operation(max_retries=3, delay=2.0)
            def sensitive_operation():
                try:
                    # 步骤1：验证通知栏整体元素存在
                    notification_div = page.wait_for_selector(
                        "#notification",
                        state="visible",
                        timeout=5000  # 5秒超时
                    )

                    # 步骤2（可选）：进一步验证内部关键元素
                    notification_btn = page.locator("#notification_btn")
                    assert notification_btn.is_visible(), "通知按钮不可见"

                    logging.info("通知栏元素验证成功")

                except Exception as e:
                    logging.error(f"通知栏验证失败: {str(e)}")
                    raise  # 触发重试机制

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
