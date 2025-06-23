import base64, hashlib, string, random
from cryptography.fernet import Fernet

class Security:
    @staticmethod
    def check_password():
        return True

    @staticmethod
    def generate_key(password: str) -> bytes:
        digest = hashlib.sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(digest)

    @staticmethod
    def encrypt(data: str, key: bytes) -> str:
        return Fernet(key).encrypt(data.encode()).decode()

    @staticmethod
    def decrypt(data: str, key: bytes) -> str:
        return Fernet(key).decrypt(data.encode()).decode()
    
    def password_generator():
        length = input("Enter password length (default 16): ").strip()
        try:
            length = int(length)
        except:
            length = 16
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for _ in range(length))
        return password
