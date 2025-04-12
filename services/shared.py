from helpers.typing_effect import typing_output
from helpers.helpers import save_contacts
from rich.console import Console
from rich.table import Table
from rich import box
from data.state import book
import time
from helpers.matrix_effect import matrix_drop

console = Console()  # Initialize Console for rich output


# GREETING
def greeting():
    """Function to greet the user"""
    print("")
    typing_output("Welcome to the Assistant Bot 💻")
    print("")
    typing_output("Loading... Please wait...")
    print("")


# HELLO
def hello():
    """Function to greet the user"""
    print("")
    typing_output("Hello, Neo...  ")
    typing_output("I am your assistant bot. ")
    typing_output("I can help you with your contacts and notes. ")
    typing_output('To see the list of available commands, please type "help". ')
    print("")


# SHOW HELP
def show_help():
    # === CONTACTS ===
    contacts_table = Table(
        show_header=True,
        header_style="bold blue",  # Customize header style
        box=box.ROUNDED,  # Customize table shape
        title="Available Commands",  # Title for the table
        title_justify="center",  # Center the title
        title_style="bold magenta",  # Title style
    )
    contacts_table.add_column("Command", style="yellow", width=20)
    contacts_table.add_column("Description", style="cyan italic")

    # Define the commands and their descriptions
    contact_commands = {
        "add contact": "Adds a new contact.",
        "find contact": "Finds a contact by name.",
        "all contacts": "Shows all contacts.",
        "all birthdays": "Shows all upcoming birthdays for the next week.",
        "edit contact": "Edit existing contact",
        "delete contact": "Delete existing contact",
        "expand contact": "Add info to existing contact",
        "show contact": "Show info for existing contact",
        "export contacts": "Exports all contacts to a CSV file.",
    }

    for command, description in contact_commands.items():
        contacts_table.add_row(command, description)

    # Display the table
    console.print("\n")
    console.print(contacts_table)
    console.print("\n")

    # === NOTES ===
    notes_table = Table(
        show_header=True,
        header_style="bold blue",  # Customize header style
        box=box.ROUNDED,  # Customize table shape
        title="Notes Commands",  # Title for the table
        title_justify="center",  # Center the title
        title_style="bold magenta",  # Title style
    )
    notes_table.add_column("Command", style="yellow", width=20)
    notes_table.add_column("Description", style="cyan italic")
    # Define the commands and their descriptions
    notes_commands = {
        "all notes": "Shows all notes.",
        "add note": "Adds a new note.",
        "find note": "To find some not with keyword",
        "change note": "Updates an existing note.",
        "delete note": "Removes an existing note.",
        "export notes": "Exports all contacts to a CSV file.",
        "show note": "Shows a specific note.",
    }
    for command, description in notes_commands.items():
        notes_table.add_row(command, description)
    # Display the table
    console.print(notes_table)
    console.print("\n")

    # === GENERAL ===
    general_table = Table(
        show_header=True,
        header_style="bold blue",  # Customize header style
        box=box.ROUNDED,  # Customize table shape
        title="General Commands",  # Title for the table
        title_justify="center",  # Center the title
        title_style="bold magenta",  # Title style
    )
    general_table.add_column("Command", style="yellow", width=20)
    general_table.add_column("Description", style="cyan italic")
    # Define the commands and their descriptions
    general_commands = {
        "hello": "Greets the user.",
        "help": "Shows the list of available commands.",
        "close/exit/quit": "Closes the bot.",
    }
    for command, description in general_commands.items():
        general_table.add_row(command, description)
    # Display the table
    console.print(general_table)
    console.print("\n")


# CLOSE
def close():
    save_contacts(book)
    typing_output("Goodbye 🐇")
    typing_output("All data saved! 💾")
    return 0


# GOODBYE
def goodbye():
    typing_output("Goodbye, Neo...  ")
    close()
    time.sleep(2)
    matrix_drop()
