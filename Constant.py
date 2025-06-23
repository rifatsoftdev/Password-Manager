class Colors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"

class Config:
    DB_NAME = "../accounts.db"
    JSON_FILE = "../account.json"

class Messages:
    WELCOME = f"{Colors.GREEN}Welcome to the Password Manager!{Colors.RESET}"
    EXIT = f"{Colors.RED}👋 Goodbye!{Colors.RESET}"
    INVALID_OPTION = f"{Colors.RED}❌ Invalid option. Try again.{Colors.RESET}"
    ACCOUNT_NOT_FOUND = f"{Colors.RED}❌ Account not found.{Colors.RESET}"
    ACCOUNT_DELETED = f"{Colors.GREEN}✅ Account deleted successfully!{Colors.RESET}"
    ACCOUNT_UPDATED = f"{Colors.GREEN}✅ Account updated successfully!{Colors.RESET}"
    ACCOUNT_ADDED = f"{Colors.GREEN}✅ Account added successfully!{Colors.RESET}"
    MASTER_PASSWORD_SET = f"{Colors.GREEN}Master password set! Restart the program.{Colors.RESET}"
    MASTER_PASSWORD_PROMPT = f"{Colors.RED}Enter Your Master Password: {Colors.RESET}"
    MASTER_PASSWORD_INCORRECT = f"{Colors.RED}Incorrect password. Try again.{Colors.RESET}"
    MASTER_PASSWORD_TOO_SHORT = f"{Colors.RED}Password too short. Use at least 8 characters.{Colors.RESET}"
    MASTER_PASSWORD_MISMATCH = f"{Colors.RED}Passwords do not match. Try again.{Colors.RESET}"
    MASTER_PASSWORD_ATTEMPTS_EXCEEDED = f"{Colors.RED}Too many failed attempts. Exiting.{Colors.RESET}"