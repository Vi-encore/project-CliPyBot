import pickle
from pathlib import Path
from models.contact import AddressBook

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