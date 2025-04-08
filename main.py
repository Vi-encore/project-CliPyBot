from colorama import Fore, Back, Style
from services import contacts, notes
from helpers.helpers import parse_input


def main():
    """
    Main function for the assistant bot
    takes following commands:add
    - hello - greets the user
    - add <name> <phone> - adds a contact
    - change <name> <old_phone> <new_phone> - replace phone number
    - phone <name> - shows all phones of a contact
    - all - shows all contacts
    - add-birthday <name> <birthday>- add birthday to the contact
    - show-birthday <name> - show birthday date of the contact
    - birthdays - show all upcoming birthdays for the next week (workdays)
    - close/exit - closes the bot
    """
    print(
        Back.LIGHTWHITE_EX
        + Fore.BLACK
        + "Welcome to the assistant bot!"
        + Style.RESET_ALL
    )
    print("")
    while True:
        user_input = input(Fore.BLUE + "Enter a command: " + Style.RESET_ALL)
        if user_input.strip() == "":
            print(Fore.YELLOW + "Please enter a command.")
            continue

        cmd, *args = parse_input(user_input)

        if cmd == "":
            print(Fore.YELLOW + "Please enter a command.")
            continue
        elif cmd in ["close", "exit"]:
            contacts.close()
            break
        elif cmd == "hello":
            print(
                Fore.GREEN
                + "Hello! I am your assistant, how can I help you?"
                + Style.RESET_ALL
            )
        # Contact commands
        elif cmd == "add contact":  # ()
            contacts.add()
        elif cmd == "remove contact":  # (name)
            contacts.remove(*args)
        elif cmd == "all contacts":  # ()
            contacts.all()
        elif cmd == "add phone":  # (name, phone number)
            contacts.add_phone(*args)
        elif cmd == "change phone":  # (name, old phone number , new phone number)
            contacts.change_phone(*args)
        elif cmd == "show phone":  # (name)
            contacts.show_phone(*args)
        elif cmd == "delete phone":  # (name, phone number)
            contacts.delete_phone(*args)
        elif cmd == "add email":  # (name, email)
            contacts.add_email(*args)
        elif cmd == "change email":  # (name, old email, new email)
            contacts.change_email(*args)
        elif cmd == "show email":  # (name)
            contacts.show_email(*args)
        elif cmd == "delete email":  # (name, email)
            contacts.delete_email(*args)
        elif cmd == "add birthday":  # (name, birthday)
            contacts.add_birthday(*args)
        elif cmd == "show birthday":  # (name)
            contacts.show_birthday(*args)
        elif cmd == "update birthday":  # (name, new birthday)
            contacts.update_birthday(*args)
        elif cmd == "all birthdays":  # (name, days_to_upcoming)
            contacts.all_birthdays()
        # # Notes commands
        # logic for notes
        else:
            print(
                Fore.YELLOW
                + 'Unknown command. To see all the available commands, type "help".'
                + Style.RESET_ALL
            )


if __name__ == "__main__":
    main()
