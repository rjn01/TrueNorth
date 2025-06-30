import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

class EncryptionManager:
    def __init__(self):
        load_dotenv()
        key = os.getenv("ENCRYPTION_KEY")
        if not key:
            raise ValueError("ENCRYPTION_KEY not set in environment.")
        self.fernet = Fernet(key.encode())

    def encrypt(self, plaintext: str) -> bytes:
        return self.fernet.encrypt(str(plaintext).encode())

    #def decrypt(self, ciphertext: bytes) -> str:
    #    return self.fernet.decrypt(ciphertext).decode()
    def decrypt(self, ciphertext):
        if isinstance(ciphertext, memoryview):
            ciphertext = ciphertext.tobytes()
        elif isinstance(ciphertext, str):
            ciphertext = ciphertext.encode()
        elif not isinstance(ciphertext, bytes):
            raise TypeError(f"Unsupported type for decryption: {type(ciphertext)}")
        
        decrypted = self.fernet.decrypt(ciphertext).decode()

        if decrypted.isdigit():
            return int(decrypted)
        try:
            return float(decrypted)
        except ValueError:
            return decrypted


def set_encryption_key():
    load_dotenv()
    if not os.getenv("ENCRYPTION_KEY"):
        key = Fernet.generate_key().decode()
        with open(".env", "a") as f:
            f.write(f"\nENCRYPTION_KEY={key}")
