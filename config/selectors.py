"""
所有页面元素选择器集中管理
按页面/功能模块组织，支持CSS/XPath/文本选择器
"""

# 登录页面
LOGIN = {
    "username": "#username",
    "password": "#password",
    "submit_button": "button[type='submit']",
    "error_message": ".error-message"
}

# 仪表盘页面
DASHBOARD = {
    "welcome_message": "text=Welcome",
    "menu_item": lambda name: f"//li[contains(@class,'menu-item') and contains(text(),'{name}')]"
}

# 通用元素
COMMON = {
    "loading": ".spinner",
    "notification": ".notyf__message",
    "dialog": {
        "confirm": "button:has-text('Confirm')",
        "cancel": "button:has-text('Cancel')"
    }
}

def get_selector(page: str, element: str) -> str:
    """安全获取选择器的辅助函数"""
    selectors = globals().get(page.upper(), {})
    return selectors.get(element, "")
