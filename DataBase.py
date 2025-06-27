import sqlite3, json

from Security import Security
from Constant import Colors, Config, Messages


class DataBase:
    def __init__(self):
        self.sectuty = Security()
        self.GREEN = Colors.GREEN
        self.RESET = Colors.RESET

    # database creation
    def create_db():
        conn = sqlite3.connect(Config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_type TEXT,
                name TEXT,
                username TEXT,
                email TEXT,
                phone TEXT,
                password TEXT,
                date_of_birth TEXT,
                recovery_email TEXT,
                recovery_phone TEXT,
                backup_codes TEXT,
                account_create TEXT
            )
        """)
        conn.commit()
        conn.close()

    # insurt account
    def insert_account(self, master_password: str):
        key = self.sectuty.generate_key(master_password)

        data = {field: input(f"🔸 {field.replace('_', ' ').title()}: ") for field in Config.fields}
        encrypted_values = [self.sectuty.encrypt(data[field], key) for field in Config.fields]

        conn = sqlite3.connect(Config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO accounts ({', '.join(Config.fields)})
            VALUES ({', '.join(['?' for _ in Config.fields])})
        """, encrypted_values)
        conn.commit()
        conn.close()

        print(Messages.ACCOUNT_ADDED)

    # show account
    def view_account(self, master_password: str):
        key = self.sectuty.generate_key(master_password)
        
        account_type = input(Messages.ACCOUNT_TYPE).strip()
        username_email = input(Messages.USERNAME_EMAIL).strip()

        conn = sqlite3.connect(Config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts")
        rows = cursor.fetchall()
        conn.close()

        found = False

        for row in rows:
            try:
                if ((account_type == Security.decrypt(row[1], key)) and (username_email == Security.decrypt(row[3], key) or username_email == Security.decrypt(row[4], key))):
                    decrypted = {
                        "id": row[0],
                        "account_type": self.sectuty.decrypt(row[1], key),
                        "name": self.sectuty.decrypt(row[2], key),
                        "username": self.sectuty.decrypt(row[3], key),
                        "email": self.sectuty.decrypt(row[4], key),
                        "phone": self.sectuty.decrypt(row[5], key),
                        "password": self.sectuty.decrypt(row[6], key),
                        "date_of_birth": self.sectuty.decrypt(row[7], key),
                        "recovery_email": self.sectuty.decrypt(row[8], key),
                        "recovery_phone": self.sectuty.decrypt(row[9], key),
                        "backup_codes": self.sectuty.decrypt(row[10], key),
                        "account_create": self.sectuty.decrypt(row[11], key)
                    }
                    print()
                    print(f"{Colors.YELLOW}🔍 Account Details:{Colors.RESET}")
                    
                    # calculate max lengths for formatting
                    max_key_len = max(len(k.title()) for k in decrypted)
                    max_val_len = max(len(str(v)) for v in decrypted.values())
                    total_width = max_key_len + max_val_len + 7 # 7 for padding and borders

                    # top border
                    border = "═" * (total_width-2)
                    print(f"╔{border}╗")

                    # all key-value print
                    for key, value in decrypted.items():
                        key_title = key.title()
                        print(f"║ {key_title:<{max_key_len}} : {str(value):<{max_val_len}} ║")

                    # buttom border
                    print(f"╚{border}╝")

                    found = True
            except Exception:
                continue

        if not found:
            print(Messages.ACCOUNT_NOT_FOUND)
            return

    # edit account
    def edit_account(self, master_password: str):
        key = self.sectuty.generate_key(master_password)
        
        account_id = input(f"✏️ Enter Account ID to Edit: {Colors.RESET}").strip()

        conn = sqlite3.connect(Config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        row = cursor.fetchone()

        if not row:
            print(f"{Colors.RED}❌ ID not found.\n{Colors.RESET}")
            return

        print(f"{Colors.CYAN}🔁 Leave field blank to keep existing value.{Colors.RESET}")
        updates = {}

        for i, field in enumerate(Config.fields, start=2):
            try:
                current_value = self.sectuty.decrypt(row[i], key)
            except Exception:
                print(f"{Colors.RED}❌ Wrong password or corrupted data.\n{Colors.RESET}")
                return

            new_value = input(f"🔸 {field.replace('_', ' ').title()} (current: {Colors.BLUE}{current_value}{Colors.RESET}): ").strip()
            updates[field] = self.sectuty.encrypt(new_value, key) if new_value else row[i]

        update_values = list(updates.values()) + [account_id]
        cursor.execute(f"""
            UPDATE accounts SET {', '.join([f"{field} = ?" for field in Config.fields])}
            WHERE id = ?
        """, update_values)
        conn.commit()
        conn.close()

        print(f"{Colors.GREEN}{Messages.ACCOUNT_UPDATED}\n{Colors.RESET}")

    # find account
    def find_account(self, master_password: str):
        key = self.sectuty.generate_key(master_password)
        
        account_type = self.sectuty.encrypt(input(Messages.ACCOUNT_TYPE).strip(), key)

        conn = sqlite3.connect(Config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE account_type = ?", (account_type,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print(f"{Colors.RED}❌ No accounts found for this type.{Colors.RESET}")
            return
        print(f"{Colors.GREEN}{len(rows)} accounts found.{Colors.RESET}")

    # delete account
    def delete_account(self, master_password: str):
        key = self.sectuty.generate_key(master_password)
        
        account_id = input(f"{Colors.RED}Enter Account ID to Delete: {Colors.RESET}").strip()
        if (account_id == "1"):
            print(Messages.PERMISSION_DENIED)
            return
        confirm = input(f"{Colors.RED}Are you sure you want to delete this account? (yes/no): {Colors.RESET}").strip().lower()
        if confirm != 'yes':
            print(f"{Colors.RED}Deletion cancelled.{Colors.RESET}")
            return
        
        conn = sqlite3.connect(Config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        row = cursor.fetchone()

        if not row:
            print(f"{Colors.RED}❌ ID not found.\n{Colors.RESET}")
            return

        cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
        conn.commit()
        conn.close()

        print(f"{Colors.GREEN}{Messages.ACCOUNT_DELETED}\n{Colors.RESET}")
