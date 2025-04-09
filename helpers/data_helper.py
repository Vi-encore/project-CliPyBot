import pickle
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
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
