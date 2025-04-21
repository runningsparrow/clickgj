# 在 config/settings.py 顶部添加
from dotenv import load_dotenv

from config.credentials import SecurityError

load_dotenv()  # 加载.env文件
import os
from pathlib import Path
import platform

# 基础配置
# BASE_URL = "https://www.jisilu.cn/"  # 替换为您的实际目标网址
# TIMEOUT = 30  # 默认超时时间(秒)

# ==================== 基础配置 ====================
BASE_URL = os.getenv('BASE_URL', 'https://www.xxxxxx.cn/')  # 从.env读取，带默认值
TIMEOUT = int(os.getenv('TIMEOUT', '30'))  # 超时时间(秒)

# 路径配置
BASE_DIR = Path(__file__).parent.parent
LOG_DIR = BASE_DIR / "logs"
SCREENSHOT_DIR = LOG_DIR / "screenshots"

# 创建必要目录
for directory in [LOG_DIR, SCREENSHOT_DIR]:
    directory.mkdir(exist_ok=True, parents=True)


# 凭证配置（从环境变量读取，带类型提示）
class Credentials_user:
    # @staticmethod
    # def get_username() -> str:
    #     return os.getenv('LOGIN_USER', 'default_user')  # 生产环境建议移除默认值

    @staticmethod
    def get_username() -> str:
        username = os.getenv('LOGIN_USER')  # 无默认值
        if not username:
            raise ValueError("必须配置LOGIN_USER环境变量")
        return username

    @classmethod
    def validate(cls):
        """严格验证凭证格式"""
        username = cls.get_username()
        if not username.isprintable() or len(username) < 4:
            raise SecurityError("用户名格式无效")

    # @staticmethod
    # def get_password() -> str:
    #     return os.getenv('LOGIN_PASS', 'default_pass')  # 生产环境建议移除默认值

    # @classmethod
    # def validate(cls):
    #     """验证凭证是否有效"""
    #     if cls.get_username() == 'default_user' or cls.get_password() == 'default_pass':
    #         raise ValueError("未配置有效的登录凭证")


    # cls 是类方法的必需参数，代表当前类
    # @classmethod
    # def validate(cls):
    #     """验证凭证是否有效"""
    #     if cls.get_username() == 'default_user':
    #         raise ValueError("未配置有效的用户")


# 指定浏览器
# os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\xxxxxxx\python\clickgj\browsers\chromium-1161\chrome-win\chrome.exe"
# ==================== 浏览器配置 ====================
# 浏览器安装路径（从.env读取，无默认值）
PLAYWRIGHT_BROWSERS_PATH = os.getenv('PLAYWRIGHT_BROWSERS_PATH')
if PLAYWRIGHT_BROWSERS_PATH:
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = PLAYWRIGHT_BROWSERS_PATH


# 浏览器配置
# IS_WINDOWS = platform.system() == "Windows"
# BROWSER_CONFIG = {
#     "headless": True,  # 后台运行
#     "slow_mo": 500,  # 操作间隔(毫秒)
#     "channel": "chrome" if IS_WINDOWS else None,
#     "args": ["--no-sandbox"] if not IS_WINDOWS else []
# }

# 浏览器启动参数
IS_WINDOWS = platform.system() == "Windows"
BROWSER_CONFIG = {
    "headless": os.getenv('HEADLESS', 'true').lower() == 'true',  # 从.env读取
    "slow_mo": int(os.getenv('SLOW_MO', '500')),  # 操作延迟(毫秒)
    "channel": os.getenv('BROWSER_CHANNEL', 'chrome' if IS_WINDOWS else None),
    "args": ["--no-sandbox"] if not IS_WINDOWS else []
}

# 日志配置
# LOGGING = {
#     "level": "INFO",
#     "format": "%(asctime)s - %(levelname)s - %(message)s",
#     "filename": LOG_DIR / "automation.log"
# }
# ==================== 日志配置 ====================
LOGGING = {
    "level": os.getenv('LOG_LEVEL', 'INFO'),
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "filename": LOG_DIR / os.getenv('LOG_FILE', 'automation.log')
}
