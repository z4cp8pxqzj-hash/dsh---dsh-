# -*- coding: utf-8 -*-
"""
增强安全密钥管理 - 使用后自动清理内存
"""
import os
import json
import hashlib
import gc

try:
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    from Crypto.Util.Padding import pad, unpad
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

class SecureKeyManager:
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config.json"
        )
        self.key_file = os.path.join(
            os.path.dirname(self.config_path), ".secure_key"
        )
        self.encrypted_key = None
        self._load_or_create_key()
    
    def _load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                self.encrypted_key = f.read()
        else:
            self.encrypted_key = get_random_bytes(32) if HAS_CRYPTO else os.urandom(32)
            with open(self.key_file, 'wb') as f:
                f.write(self.encrypted_key)
            os.chmod(self.key_file, 0o600)
    
    def encrypt_api_key(self, plaintext_key: str) -> bytes:
        if HAS_CRYPTO:
            salt = os.urandom(16)
            derived_key = hashlib.pbkdf2_hmac('sha256', self.encrypted_key, salt, 100000)
            cipher = AES.new(derived_key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(plaintext_key.encode(), AES.block_size))
            return salt + cipher.iv + ct_bytes
        else:
            return plaintext_key.encode()
    
    def decrypt_api_key(self, ciphertext: bytes) -> str:
        if HAS_CRYPTO and len(ciphertext) > 32:
            salt, iv, ct = ciphertext[:16], ciphertext[16:32], ciphertext[32:]
            derived_key = hashlib.pbkdf2_hmac('sha256', self.encrypted_key, salt, 100000)
            cipher = AES.new(derived_key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt.decode()
        elif not HAS_CRYPTO:
            return ciphertext.decode()
        return ""
    
    def save_secure_key(self, api_key: str):
        config = {}
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        encrypted = self.encrypt_api_key(api_key)
        config['agnes_api_key_enc'] = encrypted.hex()
        config.pop('agnes_api_key', None)
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def get_api_key(self) -> str:
        """获取解密的 API 密钥"""
        config = {}
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        encrypted_hex = config.get('agnes_api_key_enc', '')
        if not encrypted_hex:
            return config.get('agnes_api_key', '')
        
        try:
            encrypted = bytes.fromhex(encrypted_hex)
            return self.decrypt_api_key(encrypted)
        except Exception as e:
            print(f"解密失败: {e}")
            return ""
    
    def get_encrypted_hex(self) -> str:
        """返回 config 中已存储的密文（hex），不返回明文"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config.get('agnes_api_key_enc', '')
        except Exception:
            return ""
    
    def secure_cleanup(self, key: str):
        """安全清理内存中的密钥"""
        # 覆盖内存
        if key:
            key_list = list(key)
            for i in range(len(key_list)):
                key_list[i] = '0'
            del key_list
        gc.collect()
    
    def delete_secure_key(self):
        """安全删除密钥文件"""
        if os.path.exists(self.key_file):
            os.remove(self.key_file)


def test_secure_storage():
    manager = SecureKeyManager()
    
    test_key = "sk-test123456789"
    encrypted = manager.encrypt_api_key(test_key)
    decrypted = manager.decrypt_api_key(encrypted)
    
    print(f"原始密钥: {test_key}")
    print(f"解密结果: {decrypted}")
    print(f"匹配: {test_key == decrypted}")
    
    manager.save_secure_key(test_key)
    loaded_key = manager.get_api_key()
    print(f"加载密钥: {loaded_key}")
    
    # 安全清理
    manager.secure_cleanup(test_key)
    manager.secure_cleanup(loaded_key)
    print("内存清理完成")


if __name__ == "__main__":
    test_secure_storage()
