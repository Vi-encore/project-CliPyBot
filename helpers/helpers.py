import pickle
from pathlib import Path
from models.contact import AddressBook

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# to parse the user input from CLI
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

# get path of the file
def get_data_path(filename: str) -> Path:
    return DATA_DIR / filename


def save_data(data_object, filename: str):
    file_path = get_data_path(filename)
    with open(file_path, "wb") as f:
        pickle.dump(data_object, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
    
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