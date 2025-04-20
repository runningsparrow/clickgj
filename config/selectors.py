"""
所有页面元素选择器集中管理
按页面/功能模块组织，支持CSS/XPath/文本选择器
更新于2025-04-19 - 适配集思录网站
"""

# 登录页面
LOGIN = {
    "username": "input[name='user_name']",  # 用户名输入框
    "password": "input[name='password']",  # 密码输入框
    "submit_button": "a.btn.btn-jisilu:has-text('登录')",  # 登录按钮
    "remember_me": "input[name='auto_login']",  # 记住我复选框
    "agree_terms": "div.user_agree > input[type='checkbox']",  # 用户协议复选框
    "login_link": "a.btn.btn-default:has-text('登录')"  # 首页的登录入口链接
}

# 仪表盘/登录后页面
DASHBOARD = {
    "inbox_button": "a#index_btn.btn.btn-default[href='/inbox/']",  # 私信按钮(登录成功标志)
    "unread_badge": "#inbox_unread",  # 未读消息徽章
    "menu_item": lambda name: f"//li[contains(@class,'menu-item') and contains(text(),'{name}')]"  # 通用菜单项
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
    """
    安全获取选择器的辅助函数
    示例: get_selector('login', 'username') -> "input[name='user_name']"
    """
    selectors = globals().get(page.upper(), {})

    # 处理嵌套字典(如COMMON中的dialog)
    if isinstance(selectors, dict) and '.' in element:
        keys = element.split('.')
        value = selectors
        for key in keys:
            value = value.get(key, "")
        return value

    return selectors.get(element, "")
