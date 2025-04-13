import pickle
from pathlib import Path

# Define the directory to store data files
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_data_path(filename: str) -> Path:
    """
    Get the full path of the data file.

    Args:
        filename (str): The name of the file to retrieve the path for.

    Returns:
        Path: The full path to the specified file within the data directory.
    """
    return DATA_DIR / filename


def save_data(data_object, filename: str) -> None:
    """
    Save data to a file using pickle serialization.

    Args:
        data_object: The data object to be saved.
        filename (str): The name of the file where the data will be saved.

    This function serializes the data object and stores it in the specified file
    within the data directory.
    """
    file_path = get_data_path(filename)
    with open(file_path, "wb") as f:
        pickle.dump(data_object, f)


def load_data(filename: str, default_factory=None):
    """
    Load data from a file using pickle deserialization.

    Args:
        filename (str): The name of the file to load the data from.
        default_factory (optional): A callable to generate default data if the
                                    file doesn't exist. Defaults to None.

    Returns:
        The deserialized data object if the file exists. Otherwise, returns the
        result of `default_factory` if provided, or None.
    """
    file_path = get_data_path(filename)
    if file_path.exists():
        with open(file_path, "rb") as f:
            return pickle.load(f)
    return default_factory() if default_factory else None
