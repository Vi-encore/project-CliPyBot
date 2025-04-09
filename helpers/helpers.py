from models.contact import AddressBook
from helpers.data_helper import save_data, load_data


def parse_input(user_input):
    parts = user_input.strip().split()

    if len(parts) >= 2:
        cmd = f"{parts[0].lower()} {parts[1].lower()}"  # support 2-word commands
        args = parts[2:]
    else:
        cmd = parts[0].lower() if parts else ""
        args = parts[1:] if len(parts) > 1 else []

    return [cmd] + args

def save_contacts(book):
    save_data(book, "contacts.pkl")

def load_contacts():
    return load_data("contacts.pkl", AddressBook)

def save_notes(notes):
    save_data(notes, "notes.pkl")

def load_notes():
    return load_data("notes.pkl", dict)