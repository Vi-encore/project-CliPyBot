import re

def validate_and_normalize_phone(phone: str) -> str | None:
    pre_normalize = re.sub(r"[^0-9+]", "", phone)
    if re.search(r"^\+", pre_normalize):
        normalized_phone = pre_normalize
    elif re.search(r"^380", pre_normalize):
        normalized_phone = f"+{pre_normalize}"
    else:
        normalized_phone = f"+38{pre_normalize}"

    if not normalized_phone or not re.search(r'^\+\d+$', normalized_phone):
        return None
    if normalized_phone.startswith('+38') and len(normalized_phone) != 13:
        return None

    return normalized_phone



def standardize_name(name: str) -> str:
    name = name.strip()

    if not re.fullmatch(r'[a-zA-Z][a-zA-Z0-9 ]*[a-zA-Z0-9]', name):
        return None
    name = ' '.join(word.capitalize() for word in name.split())
    return name