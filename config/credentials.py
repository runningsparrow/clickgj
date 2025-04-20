# config/credentials.py
import os
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv


# 自定义异常类
class SecurityError(Exception):
    """用于加密/解密相关的安全异常"""
    pass


load_dotenv()  # 加载.env文件


class SecureCredentials:
    _key = os.getenv('SAFE_KEY')  # 先获取为字符串

    @classmethod
    def get_password(cls) -> str:
        """安全获取解密后的密码"""
        try:
            if not cls._key:
                raise SecurityError("未配置加密密钥(SAFE_KEY)")

            encrypted = os.getenv('ENC_PASSWORD')
            if not encrypted:
                raise ValueError("未配置加密密码(ENC_PASSWORD)")

            # 将密钥和密文转为bytes
            key = cls._key.encode()
            cipher_suite = Fernet(key)
            return cipher_suite.decrypt(encrypted.encode()).decode()

        except InvalidToken:
            raise SecurityError("解密失败：密钥与密文不匹配或已损坏")
        except Exception as e:
            raise RuntimeError(f"凭证解密错误: {str(e)}")