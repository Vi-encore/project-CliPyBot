import re


def validate_and_normalize_phone(phone: str) -> str | None:
    """
    Validate and normalize a phone number to a standard international format.

    The function removes non-numeric characters, ensures the phone number starts
    with a valid prefix (e.g., '+', '380', or '+38'), and checks its length for
    validity if it starts with '+38'.

    Args:
        phone (str): The phone number string to validate and normalize.

    Returns:
        str | None: The normalized phone number as a string if valid.
                    Returns None if the phone number is invalid.
    """
    pre_normalize = re.sub(
        r"[^0-9+]", "", phone
    )  # Remove all non-numeric characters except '+'
    if re.search(r"^\+", pre_normalize):  # Starts with '+'
        normalized_phone = pre_normalize
    elif re.search(r"^380", pre_normalize):  # Starts with '380'
        normalized_phone = f"+{pre_normalize}"
    else:  # Assume Ukrainian phone number and add '+38'
        normalized_phone = f"+38{pre_normalize}"

    # Validate the normalized phone number
    if not normalized_phone or not re.search(r"^\+\d+$", normalized_phone):
        return None
    if normalized_phone.startswith("+38") and len(normalized_phone) != 13:
        return None

    return normalized_phone


def standardize_name(name: str) -> str | None:
    """
    Standardize a name to ensure it's formatted correctly.

    The function removes any leading or trailing whitespace, validates the name
    to contain only alphanumeric characters (starting with a letter), and
    capitalizes the first letter.

    Args:
        name (str): The name string to validate and standardize.

    Returns:
        str | None: The standardized name as a string if valid.
                    Returns None if the name is invalid.
    """
    name = name.strip()  # Remove leading and trailing whitespace

    # Validate name format (must start with a letter and contain only alphanumeric characters)
    if not re.fullmatch(r'[a-zA-Z][a-zA-Z0-9 ]*[a-zA-Z0-9]', name):
        return None
    name = ' '.join(word.capitalize() for word in name.split())
    return name
