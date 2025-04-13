all_available_commands = [
    "add contact",
    "find contact",
    "all contacts",
    "all birthdays",
    "edit contact",
    "delete contact",
    "expand contact",
    "show contact",
    "export contacts",
    "all notes",
    "add note",
    "find note",
    "change note",
    "delete note",
    "export notes",
    "show note",
]


def commands() -> list[str]:
    """
    Retrieves the list of all available commands for the assistant bot.

    The commands encompass functionalities for managing contacts
    and notes, such as adding, editing, finding, deleting, and exporting data.

    Returns:
        list[str]: A list of string commands supported by the bot.
    """
    return all_available_commands


commands_list = commands()
