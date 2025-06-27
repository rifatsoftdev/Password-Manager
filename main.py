import getpass, pyfiglet
from termcolor import colored

from DataBase import DataBase
from Constant import Colors, Config, Messages
from Security import Security


# title text function
def title_text(txt):
    title = pyfiglet.figlet_format(txt)
    print(colored(title, color="blue"))

def main():
    db = DataBase()

    if (not Security.check_database()):
        DataBase.create_db()
        password = getpass.getpass(f"{Colors.RED}Enter Master Password: {Colors.RESET}")
        confrem_password = getpass.getpass(f"{Colors.RED}Reenter Master Password: {Colors.RESET}")

        if (password == confrem_password):
            Security.create_password(confrem_password)
        else:
            print(f"{Messages.MASTER_PASSWORD_MISMATCH}")

    master_password = getpass.getpass(Messages.MASTER_PASSWORD_PROMPT)

    # check password
    if (not(Security.check_password(master_password))):
        print(f"{Colors.RED}{Messages.MASTER_PASSWORD_INCORRECT}{Colors.RESET}")
        main()

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
            print(f"\n{Colors.GREEN}Genarated Password is : {Security.password_generator()}{Colors.RESET}")
        elif choice == "7":
            print(Messages.EXIT)
            break
        else:
            print(Messages.INVALID_OPTION)

# Start here
if __name__ == "__main__":
    # title_text("Password Manager")
    print(Messages.WELCOME)
    main()