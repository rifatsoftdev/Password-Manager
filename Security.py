import base64, hashlib, string, random, os, sqlite3
from cryptography.fernet import Fernet

from Constant import Config, Colors


class Security:
    @staticmethod
    def create_password(master_password: str):
        key = Security.generate_key(master_password)

        data = {field: "admin" for field in Config.fields}
        encrypted_values = [Security.encrypt(value, key) for value in data.values()]

        conn = sqlite3.connect(Config.DB_NAME)
        cursor = conn.cursor()

        # Insert query
        cursor.execute(f"""
            INSERT INTO accounts ({', '.join(Config.fields)})
            VALUES ({', '.join(['?' for _ in Config.fields])})
        """, encrypted_values)

        conn.commit()
        conn.close()

    @staticmethod
    def check_password(master_password: str):
        key = Security.generate_key(master_password)

        conn = sqlite3.connect(Config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (1,))
        rows = cursor.fetchall()
        conn.close()

        try:
            if (Security.decrypt(rows[0][3], key) == "admin" and Security.decrypt(rows[0][6], key) == "admin"):
                return True
            else:
                return False
        except Exception:
            return False
        
    @staticmethod
    def check_database():
        return os.path.isfile(Config.DB_NAME)

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
        try:
            length = int(input("Enter password length (default 16): "))
            if (length > 30):
                return f"{Colors.RED}Password length less than or equal 30!{Colors.RED}"
            elif (length < 8):
                return f"{Colors.RED}Password length greater than or equal 8!{Colors.RED}"
        except:
            length = 16
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for _ in range(length))

        return password
