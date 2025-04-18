import os
from pathlib import Path
import platform

# 基础配置
BASE_URL = "https://www.jisilu.cn/"  # 替换为您的实际目标网址
TIMEOUT = 30  # 默认超时时间(秒)

# 路径配置
BASE_DIR = Path(__file__).parent.parent
LOG_DIR = BASE_DIR / "logs"
SCREENSHOT_DIR = LOG_DIR / "screenshots"

# 创建必要目录
for directory in [LOG_DIR, SCREENSHOT_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

# 浏览器配置
IS_WINDOWS = platform.system() == "Windows"
BROWSER_CONFIG = {
    "headless": True,  # 后台运行
    "slow_mo": 500,  # 操作间隔(毫秒)
    "channel": "chrome" if IS_WINDOWS else None,
    "args": ["--no-sandbox"] if not IS_WINDOWS else []
}

# 日志配置
LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "filename": LOG_DIR / "automation.log"
}