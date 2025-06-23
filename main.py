import sqlite3, getpass, pyfiglet, os, json, string, random
from termcolor import colored

from DataBase import DataBase
from Constant import Colors, Config, Messages
from Security import Security


# title text function
def title_text(txt):
    title = pyfiglet.figlet_format(txt)
    print(colored(title, color="blue"))


def main():
    DataBase.create_db()
    title_text("Password Manager")

    db = DataBase()
    master_password = getpass.getpass("Enter Your Master Password: ")

    while True:
        print()
        print(f"{Colors.CYAN}Menu:{Colors.RESET}")
        print(f"{Colors.YELLOW} 1. Insert New Account{Colors.RESET}")
        print(f"{Colors.YELLOW} 2. View Account{Colors.RESET}")
        print(f"{Colors.YELLOW} 3. Edit Account{Colors.RESET}")
        print(f"{Colors.YELLOW} 4. Find Account{Colors.RESET}")
        print(f"{Colors.YELLOW} 5. Delete Account{Colors.RESET}")
        print(f"{Colors.YELLOW} 6. Password Generator{Colors.RESET}")
        print(f"{Colors.YELLOW} 7. Exit{Colors.RESET}")

        choice = input(f"{Colors.MAGENTA}=> Choose an option: {Colors.RESET}").strip()

        if choice == "1":
            db.insert_account(master_password)
        elif choice == "2":
            db.view_account(master_password)
        elif choice == "3":
            db.edit_account(master_password)
        elif choice == "4":
            db.find_account(master_password)
        elif choice == "5":
            db.delete_account(master_password)
        elif choice == "6":
            Security.password_generator()
        elif choice == "7":
            print(f"{Colors.GREEN}{Messages.EXIT}{Colors.RESET}")
            break
        else:
            print(f"{Colors.RED}{Messages.INVALID_OPTION}\n{Colors.RESET}")

# Start here
if __name__ == "__main__":
    main()

    # db = DataBase()
    # password = getpass.getpass("Password: ")
    # json_file = Config.JSON_FILE
    # db.insert_json_to_sqlite(password, json_file)

