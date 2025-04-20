from cryptography.fernet import Fernet
import getpass  # 安全输入模块


def generate_encrypted_credentials():
    """交互式生成加密凭证"""
    print("\n=== 密码加密工具 ===")

    # 1. 生成密钥（首次运行时）
    key = Fernet.generate_key()
    print(f"\n🔑 生成的SAFE_KEY（保存到.env文件）:\n{key.decode()}")

    # 2. 等待用户输入密码
    while True:
        password = getpass.getpass("请输入需要加密的密码（输入为空时退出）: ")
        if not password:
            return

        # 3. 加密处理
        cipher_suite = Fernet(key)
        encrypted = cipher_suite.encrypt(password.encode())

        # 4. 输出结果
        print("\n✅ 加密完成！请将以下内容添加到.env文件：")
        print("----------------------------------------")
        print(f"SAFE_KEY={key.decode()}")
        print(f"ENC_PASSWORD={encrypted.decode()}")
        print("----------------------------------------\n")


if __name__ == "__main__":
    generate_encrypted_credentials()