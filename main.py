from fuzzywuzzy import process
from services import contacts, notes
from helpers.helpers import parse_input
from helpers.commands import commands_list
from services.shared import show_help, close, hello, goodbye, greeting
from helpers.typing_effect import typing_input, typing_output
from rich.console import Console

# Initialize Console for rich output
console = Console()


def suggest_and_execute_command(cmd: str, args: list, func) -> bool:
    """
    Suggest and execute a command based on the user's input.

    Args:
        cmd (str): The user's input command.
        args (list): Additional arguments passed along with the command.
        func (function): The function to execute the command.

    Returns:
        bool: True if a suggested command is executed, otherwise False.
    """
    if not cmd or cmd.strip() == "":
        return False

    # Get suggestion using fuzzywuzzy
    match = process.extractOne(cmd.strip().lower(), commands_list)

    if match and match[1] >= 70:  # Only consider matches with score of 70 or higher
        suggested_cmd = match[0]

        # Ask user if they want to execute the suggested command
        console.print(
            f'Did you mean "[blue]{suggested_cmd}[/]"?', style="yellow italic"
        )
        response = typing_input(f'Run "{suggested_cmd}" instead? (y/n): ')

        if response.lower() in ("y", "yes"):
            # Execute the suggested command
            func(suggested_cmd, args)
            return True

    return False


def execute_command(cmd: str, args: list) -> None:
    """
    Execute the appropriate function based on the provided command.

    Args:
        cmd (str): The command to execute.
        args (list): Additional arguments for the command.

    This function handles both contact-related and note-related commands.
    """
    if cmd == "add contact":
        contacts.add()
    elif cmd == "find contact":
        contacts.find(*args)
    elif cmd == "all contacts":
        contacts.all()
    elif cmd == "all birthdays":
        contacts.all_birthdays()
    elif cmd == "export contacts":
        contacts.export_contacts_to_csv()
    elif cmd == "edit contact":
        contacts.edit_contact()
    elif cmd == "expand contact":
        contacts.expand_contact()
    elif cmd == "show contact":
        contacts.display_contact()
    elif cmd == "delete contact":
        contacts.delete_contact()
    elif cmd == "add note":
        notes.add()
    elif cmd == "all notes":
        notes.all()
    elif cmd == "change note":
        notes.change_note()
    elif cmd == "delete note":
        notes.delete_note()
    elif cmd == "find note":
        notes.find()
    elif cmd == "show note":
        notes.display_note()
    elif cmd == "export notes":
        notes.export_notes_to_csv()


def main() -> None:
    """
    Main function for the assistant bot that interacts with users.

    This bot provides functionalities for managing contacts and notes.
    It supports various commands to add, modify, delete, and export data.
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
        elif cmd in commands_list:
            execute_command(cmd, args)

        # Notes commands
        else:
            print("")
            console.print("Unknown command ⚠️", style="red bold")
            print("")
            if not suggest_and_execute_command(cmd, args, execute_command):
                # If no suggestion was executed, show the help message
                console.print(
                    'To get info about available commands, please type [blue]"help"[/] ',
                    style="yellow italic",
                )
            print("")


if __name__ == "__main__":
    main()
