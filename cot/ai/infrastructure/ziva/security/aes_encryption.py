import base64
import os
from ....domain.interfaces.encryptor import IEncryptor
from Crypto.Cipher import AES

class AESEncryptor(IEncryptor):
    """Concrete AES implementation of encryption interface"""
    def __init__(self, encryption_key: str = None):
        self.encryption_key = base64.urlsafe_b64decode(encryption_key or os.getenv('SESSION_ENC_KEY'))
        if not self.encryption_key or len(self.encryption_key) not in (16, 24, 32):
            raise ValueError("Encryption key must be 16, 24, or 32 bytes long")
    
    def encrypt(self, data: str) -> str:
        """Encrypts data and returns base64-encoded string"""
        iv = os.urandom(16)
        cipher = AES.new(self.encryption_key, AES.MODE_CFB, iv)
        encrypted = cipher.encrypt(data.encode())
        return base64.b64encode(iv + encrypted).decode('utf-8')
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypts base64-encoded encrypted data"""
        raw = base64.b64decode(encrypted_data)
        cipher = AES.new(self.encryption_key, AES.MODE_CFB, raw[:16])
        return cipher.decrypt(raw[16:]).decode('utf-8')