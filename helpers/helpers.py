from models.contact import AddressBook
from models.note import NotesBook
from helpers.data_helper import save_data, load_data


def parse_input(user_input) -> list[str]:
    """
    Parse user input to extract the command and arguments.

    Args:
        user_input (str): The input string entered by the user.

    Returns:
        list[str]: A list where the first element is the command (str) and
                the subsequent elements are the arguments (list of strings).

    This function supports parsing two-word commands (e.g., "add contact") and
    additional arguments separated by spaces.
    """
    parts = user_input.strip().split()

    if len(parts) >= 2:
        cmd = f"{parts[0].lower()} {parts[1].lower()}"  # Support 2-word commands
        args = parts[2:]
    else:
        cmd = parts[0].lower() if parts else ""
        args = parts[1:] if len(parts) > 1 else []

    return [cmd] + args


def save_contacts(book) -> None:
    """
    Save the contact book data to a file.

    Args:
        book (AddressBook): An instance of AddressBook containing contact data.

    The data is serialized using pickle and stored in a file named 'contacts.pkl'.
    """
    save_data(book, "contacts.pkl")


def load_contacts() -> AddressBook:
    """
    Load the contact book data from a file.

    Returns:
        AddressBook: An instance of AddressBook loaded from 'contacts.pkl'.
                    If the file does not exist, a new AddressBook instance is returned.
    """
    return load_data("contacts.pkl", AddressBook)


def save_notes(notes) -> None:
    """
    Save the notes data to a file.

    Args:
        notes (NotesBook): An instance of NotesBook containing notes data.

    The data is serialized using pickle and stored in a file named 'notes.pkl'.
    """
    save_data(notes, "notes.pkl")


def load_notes() -> NotesBook:
    """
    Load the notes data from a file.

    Returns:
        NotesBook: An instance of NotesBook loaded from 'notes.pkl'.
                If the file does not exist, a new NotesBook instance is returned.
    """
    return load_data("notes.pkl", NotesBook)
