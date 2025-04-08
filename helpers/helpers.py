import pickle
from pathlib import Path
from colorama import Fore, Style
from models.contact import AddressBook
from rich.console import Console
from rich.table import Table
from rich import box
import time

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def parse_input(user_input):
    parts = user_input.strip().split()
    
    if len(parts) >= 2:
        cmd = f"{parts[0].lower()} {parts[1].lower()}"  # support 2-word commands
        args = parts[2:]
    else:
        cmd = parts[0].lower() if parts else ''
        args = parts[1:] if len(parts) > 1 else []

    return [cmd] + args  

# get path of the file
def get_data_path(filename: str) -> Path:
    return DATA_DIR / filename

def save_data(data_object, filename: str):
    file_path = get_data_path(filename)
    with open(file_path, "wb") as f:
        pickle.dump(data_object, f)
    
def load_data(filename: str, default_factory=None):
    file_path = get_data_path(filename)
    if file_path.exists():
        with open(file_path, "rb") as f:
            return pickle.load(f)
    return default_factory() if default_factory else None

# ===== Specific helpers =====

def save_contacts(book):
    save_data(book, "contacts.pkl")

def load_contacts():
    return load_data("contacts.pkl", AddressBook)

def save_notes(notes):
    save_data(notes, "notes.pkl")

def load_notes():
    return load_data("notes.pkl", dict)

# ===== Console output helpers =====

# Initialize Console for rich output
console = Console()
def show_help():
    # === CONTACTS ===
    contacts_table = Table(
        show_header=True,
        header_style="bold blue",  # Customize header style
        box=box.ROUNDED,              # Customize table shape
        title="Available Commands",  # Title for the table
        title_justify="center",      # Center the title
        title_style="bold magenta",  # Title style
    )
    contacts_table.add_column("Command", style="yellow", width=20)
    contacts_table.add_column("Description", style="cyan italic")
    
    # Define the commands and their descriptions
    contact_commands = {
        'hello': 'Greets the user.',
        'add contact': 'Adds a new contact.',
        'remove contact': 'Removes an existing contact.',
        'all contacts': 'Shows all contacts.',
        'add phone': 'Adds a phone number to a contact.',
        'change phone': 'Changes a phone number for a contact.',
        'show phone': 'Shows all phone numbers for a contact.',
        'delete phone': 'Deletes a phone number from a contact.',
        'add email': 'Adds an email to a contact.',
        'change email': 'Changes an email for a contact.',
        'show email': 'Shows all emails for a contact.',
        'delete email': 'Deletes an email from a contact.',
        'add birthday': 'Adds a birthday to a contact.',
        'show birthday': 'Shows a contact’s birthday.',
        'all birthdays': 'Shows all upcoming birthdays for the next week.',
        'export contacts': 'Exports all contacts to a CSV file.',
        'help': 'Shows the list of available commands.',
        'close': 'Closes the bot.'
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
        box=box.ROUNDED,              # Customize table shape
        title="Notes Commands",  # Title for the table
        title_justify="center",      # Center the title
        title_style="bold magenta",  # Title style
    )
    notes_table.add_column("Command", style="yellow", width=20)
    notes_table.add_column("Description", style="cyan italic")
    # Define the commands and their descriptions
    notes_commands = {
        'add note': 'Adds a new note.',
        'remove note': 'Removes an existing note.',
        'all notes': 'Shows all notes.',
        'show note': 'Shows a specific note.',
        'update note': 'Updates an existing note.'
    }
    for command, description in notes_commands.items():
        notes_table.add_row(command, description)
    # Display the table
    console.print(notes_table)
    console.print("\n")
    # === END ===
    
def typing_effect(text, color='dark_green', s_style='normal'):
    """ Function to mimic typing effect in the console with customizable color and style """
    for char in text:
        style = f"{color}"  # Initialize with color
        if s_style != 'normal':
            style += f" {s_style}"  # Add style if it's not 'normal'
        console.print(f"{char}", style=style, end='', no_wrap=True)
        time.sleep(0.04)
    # console.print()  # To move to the next line after printing the whole text

def typing_input(prompt, color='dark_green', s_style='normal'):
    """ Mimic typing effect for input prompt with customizable color and style """
    typing_effect(prompt, color, s_style)
    return console.input()  # Collect user input after the typing effect

def typing_output(output, color='green', s_style='bold'):
    """ Mimic typing effect for any printed output with customizable color and style """
    typing_effect(output, color, s_style)
    console.print()  # To move to the next line after printing the whole text