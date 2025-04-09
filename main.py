from services import contacts
from helpers.helpers import parse_input
from services.shared import show_help, close, hello, goodbye, greeting
from helpers.typing_effect import typing_input, typing_output
from rich.console import Console
from helpers.matrix_effect import matrix_drop

# Initialize Console for rich output
console = Console()


def main():
    """
    Main function for the assistant bot
    that works with contacts and notes.
    """
    greeting()

    while True:
        user_input = typing_input("Enter a command </>: ")
        if user_input.strip() == "":
            console.print("No command entered ⚠️", style="red bold")
            typing_output("Please enter a command. ", color="yellow", s_style="italic")
            print("")
            continue

        cmd, *args = parse_input(user_input)

        if cmd == "":
            console.print("Please enter a command.", style="yellow italic")
            continue
        elif cmd in ["close", "exit", "quit"]:
            close()
            break
        elif cmd == "hello":
            hello()
        elif cmd == "help":
            show_help()
        elif cmd == "goodbye":  # to close presentation
            goodbye()
            break
        # Contact commands
        elif cmd == "add contact":  # ()
            contacts.add()
        elif cmd == "find contact":  # (name)
            contacts.find(*args)
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
        elif cmd == 'all birthdays': #(name, days_to_upcoming)
            contacts.all_birthdays(*args)
        elif cmd == 'export contacts': #()
            contacts.export_contacts_to_csv()
        # Notes commands
        # logic for notes
        else:
            print("")
            console.print("Unknown command ⚠️", style="red bold")
            console.print(
                'To get info about available commands, please type [blue]"help"[/] ',
                style="yellow italic",
            )
            print("")


if __name__ == "__main__":
    main()
