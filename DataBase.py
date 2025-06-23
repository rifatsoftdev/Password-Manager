import sqlite3, json

from Security import Security
from Constant import Colors, Config


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
        account_type = input(f"{Colors.CYAN}Account Type (e.g., Gmail, Facebook): {Colors.RESET}").strip()

        fields = [
            "name", "username", "email", "phone", "password",
            "date_of_birth", "recovery_email", "recovery_phone",
            "backup_codes", "account_create"
        ]

        data = {field: input(f"🔸 {field.replace('_', ' ').title()}: ") for field in fields}
        encrypted_values = [self.sectuty.encrypt(data[field], key) for field in fields]

        conn = sqlite3.connect("accounts.db")
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO accounts (account_type, {', '.join(fields)})
            VALUES (?, {', '.join(['?' for _ in fields])})
        """, [account_type] + encrypted_values)
        conn.commit()
        conn.close()

        print(f"{Colors.GREEN}✅ Account inserted successfully!\n{Colors.RESET}")

    # show account
    def view_account(self, master_password: str):
        key = self.sectuty.generate_key(master_password)
        account_type = input(f"{Colors.CYAN}Enter Account Type: {Colors.RESET}").strip()
        user_input = input(f"{Colors.CYAN}Enter Your Email or Username: {Colors.RESET}").strip()

        conn = sqlite3.connect("accounts.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE account_type = ?", (account_type,))
        rows = cursor.fetchall()
        conn.close()

        found = False

        for row in rows:
            try:
                decrypted_username = self.sectuty.decrypt(row[3], key)
                decrypted_email = self.sectuty.decrypt(row[4], key)

                if user_input == decrypted_username or user_input == decrypted_email:
                    decrypted = {
                        "id": row[0],
                        "account_type": row[1],
                        "name": self.sectuty.decrypt(row[2], key),
                        "username": decrypted_username,
                        "email": decrypted_email,
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
            print(f"{Colors.RED}❌ No matching data found or wrong password.\n{Colors.RESET}")
            return

    # edit account
    def edit_account(self, master_password: str):
        key = self.sectuty.generate_key(master_password)
        account_id = input(f"✏️ Enter Account ID to Edit: {Colors.RESET}").strip()

        conn = sqlite3.connect("accounts.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        row = cursor.fetchone()

        if not row:
            print(f"{Colors.RED}❌ ID not found.\n{Colors.RESET}")
            return

        fields = [
            "name", "username", "email", "phone", "password",
            "date_of_birth", "recovery_email", "recovery_phone",
            "backup_codes", "account_create"
        ]

        print(f"{Colors.CYAN}🔁 Leave field blank to keep existing value.{Colors.RESET}")
        updates = {}

        for i, field in enumerate(fields, start=2):
            try:
                current_value = self.sectuty.decrypt(row[i], key)
            except Exception:
                print(f"{Colors.RED}❌ Wrong password or corrupted data.\n{Colors.RESET}")
                return

            new_value = input(f"🔸 {field.replace('_', ' ').title()} (current: {current_value}): ").strip()
            updates[field] = self.sectuty.encrypt(new_value, key) if new_value else row[i]

        update_values = list(updates.values()) + [account_id]
        cursor.execute(f"""
            UPDATE accounts SET {', '.join([f"{field} = ?" for field in fields])}
            WHERE id = ?
        """, update_values)
        conn.commit()
        conn.close()

        print(f"{Colors.GREEN}✅ Account updated successfully!\n{Colors.RESET}")

    # find account
    def find_account(self, master_password: str):
        account_type = input(f"{Colors.CYAN}Enter Account Type: {Colors.RESET}").strip()

        conn = sqlite3.connect("accounts.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE account_type = ?", (account_type,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print(f"{Colors.RED}❌ No accounts found for this type.\n{Colors.RESET}")
            return
        print(f"{Colors.GREEN}{len(rows)} accounts found.{Colors.RESET}\n")

    # delete account
    def delete_account(self, master_password: str):
        key = self.sectuty.generate_key(master_password)
        account_id = input(f"{Colors.RED}Enter Account ID to Delete: {Colors.RESET}").strip()
        confirm = input(f"{Colors.RED}Are you sure you want to delete this account? (yes/no): {Colors.RESET}").strip().lower()
        if confirm != 'yes':
            print(f"{Colors.RED}Deletion cancelled.{Colors.RESET}")
            return
        
        conn = sqlite3.connect("accounts.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        row = cursor.fetchone()

        if not row:
            print(f"{Colors.RED}❌ ID not found.\n{Colors.RESET}")
            return

        cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
        conn.commit()
        conn.close()

        print(f"{Colors.GREEN} Account deleted successfully!\n{Colors.RESET}")

    def insert_json_to_sqlite(self, master_password: str, json_file: str):
        key = self.sectuty.generate_key(master_password)

        try:
            with open(json_file, 'r') as f:
                json_data = json.load(f)
        except Exception as e:
            print(f"{Colors.RED}❌ Error reading JSON file: {e}{Colors.RESET}")
            return

        all_accounts = json_data.get("accounts", {})

        fields = [
            "name", "username", "email", "phone", "password",
            "date_of_birth", "recovery_email", "recovery_phone",
            "backup_codes", "account_create"
        ]

        total_inserted = 0

        for account_type, entries in all_accounts.items():
            for entry in entries:
                data = {}
                for field in fields:
                    value = entry.get(field, '')
                    if isinstance(value, list):
                        value = ', '.join(value)
                    data[field] = value

                encrypted_values = [self.sectuty.encrypt(data[field], key) for field in fields]

                try:
                    conn = sqlite3.connect("accounts.db")
                    cursor = conn.cursor()
                    cursor.execute(f"""
                        INSERT INTO accounts (account_type, {', '.join(fields)})
                        VALUES (?, {', '.join(['?' for _ in fields])})
                    """, [account_type] + encrypted_values)
                    conn.commit()
                    conn.close()
                    total_inserted += 1
                except Exception as e:
                    print(f"{Colors.RED}❌ Failed to insert entry for '{account_type}': {e}{Colors.RESET}")

        print(f"{self.GREEN}✅ Total {total_inserted}accounts inserted from JSON!{self.RESET}")
