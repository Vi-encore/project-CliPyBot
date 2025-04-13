import csv
from typing import Literal
from pathlib import Path
import datetime as dt
from datetime import datetime as dtdt
from decorators.decorators import input_error, check_arguments
from helpers.validators import validate_and_normalize_phone, validate_email_str, validate_date_str
from models.contact import Record
from helpers.helpers import save_contacts
from rich.console import Console
from helpers.create_table import (
    show_contact_in_table,
    show_all_contacts_table,
    show_birthdays_table,
    show_options_for_query,
)
from helpers.typing_effect import typing_output, typing_input
from data.state import book

console = Console()


def no_record_message(name: str) -> None:
    """
    Display a message when a contact is not found.

    Args:
        name (str): Name of the contact that was not found.

    Returns:
        None
    """
    typing_output(f'Contact "{name}" not found.❗', color="yellow")
    return


def show_contact(record) -> None:
    """
    Display a single contact's details in a formatted table.

    Args:
        record (Record): The contact record to display.

    Returns:
        None
    """
    print("")
    show_contact_in_table(record)
    print("")
    return


# ===============
# === RECORD ===
# ===============


# ADD NEW CONTACT
@input_error
def add() -> Literal[1, 0]:
    """
    Add a new contact to the address book with details like name, phone, email, birthday and address.

    This function interactively prompts the user for contact information and validates the input.
    If a contact with the provided name already exists, it updates that contact.

    Returns:
        int: 0 for success, 1 for failure
    """
    name = typing_input("Contact name: (str): ")
    if not name:
        console.print("Name is required to create a contact. ❗", style="red")
        return 1

    record = book.find_by_name(name)
    if not record:
        record = Record(name)
        book.add_record(record)
        typing_output("New contact created.")
    else:
        typing_output("Contact already exists.")
        typing_output("Updating details...")

    # Loop for phone
    while True:
        phone = typing_input("Contact phone (press Enter to skip): (num) ").strip()
        if not phone:
            break
        try:
            record.add_phone(phone)
            break
        except Exception as e:
            console.print("Invalid phone.❗ ", style="red")
            typing_output("Please try again. ", color="yellow")

    # Loop for email
    while True:
        email = typing_input("Contact email (press Enter to skip): (str): ").strip()
        if not email:
            break
        try:
            record.add_email(email)
            break
        except Exception as e:
            console.print("Invalid email ❗ ", style="red")
            typing_output("Please try again. ", color="yellow")

    # Loop for birthday
    while True:
        birthday = typing_input(
            "Contact birthday (dd.mm.yyyy, press Enter to skip): (str) "
        ).strip()
        if not birthday:
            break
        try:
            record.add_birthday(birthday)
            break
        except Exception as e:
            console.print("Invalid birthday format.❗ ", style="red")
            typing_output("Please use the format dd.mm.yyyy. ", color="yellow")

    # Loop for address
    while True:
        address = typing_input("Contact address (press Enter to skip): (str) ").strip()
        if not address:
            break
        try:
            record.add_address(address)
            break
        except Exception as e:
            console.print("Invalid address format.❗ ", style="red")
            typing_output(f"Please use the format dd.mm.yyyy. ", color="yellow")

    save_contacts(book)

    typing_output(f'Contact "{name}" saved successfully. ✅', color="green")
    show_contact(record)  # show contact details in table
    return 0


# FIND CONTACT
@input_error
def find() -> Literal[1, 0]:
    """
    Find contacts based on various search criteria.

    Allows searching for contacts by name, phone, email, birthday, or address.
    Displays search options and prompts the user for search parameters.

    Returns:
        int: 0 for success, 1 for failure or no results
    """
    print("")
    show_options_for_query()
    print("")

    # Loop for query
    while True:
        query = (
            typing_input(
                "How do you want to search (Enter the number of field): (num) "
            )
            .strip()
            .lower()
        )

        if not query:
            typing_output("No input provided❗", color="yellow")
            typing_output("You can enter any other command")
            return 1

        if query not in ["1", "2", "3", "4", "5"]:
            typing_output(
                "Invalid option. Please enter a number between 1 and 5. ❗",
                color="yellow",
            )
            continue
        break

    # Get args based on query
    if query == "1":  # search by name
        args = typing_input("Enter the name of the contact: (str): ").strip().split()
    elif query == "2":
        args = typing_input("Enter the phone number: (num): ").strip().split()
    elif query == "3":
        args = typing_input("Enter the email address: (str): ").strip().split()
    elif query == "4":
        args = typing_input("Enter the birthday (dd.mm.yyyy): (str): ").strip().split()
    elif query == "5":
        args = typing_input("Enter the address: (str): ").strip().split()
    else:
        typing_output(
            "Invalid option. Please enter a number between 1 and 5. ❗", color="yellow"
        )
        return 1
    if not args:
        typing_output(
            "No input provided. Please enter a valid query. ❗", color="yellow"
        )
        return 1

    # Call the find method with the appropriate arguments
    if query == "1":  # search by name
        result = book.find(" ".join(args), by_name=True)
    elif query == "2":  # search by phone
        result = book.find(" ".join(args), by_phone=True)
    elif query == "3":  # search by email
        result = book.find(" ".join(args), by_email=True)
    elif query == "4":  # search by birthday
        result = book.find(" ".join(args), by_birthday=True)
    elif query == "5":
        result = book.find(" ".join(args), by_address=True)
    else:
        typing_output(
            "Invalid option. Please enter a number between 1 and 5. ❗", color="yellow"
        )
        return 1

    if not result:
        typing_output("No record found. ❗", color="yellow")
        return 1
    # If a record is found, show the contact details

    print("")
    typing_output("Contact found:")
    show_all_contacts_table(result)  # show contacts details in table
    print("")
    return 0


# REMOVE CONTACT
@check_arguments(1)
@input_error
def remove(*args: tuple) -> Literal[1, 0]:
    """
    Remove a contact from the address book.

    Args:
        *args (tuple): Variable length argument list containing the name of the contact to remove.

    Returns:
        int: 0 for success, 1 for failure
    """
    name = " ".join(args)

    record = book.find_by_name(name)

    if not record:
        no_record_message(name)
        typing_output(f"Cannot delete contact. 🚫", color="yellow")
        return 1

    typing_output("Contact found:")
    show_contact(record)  # show contact details in table

    confirmation = (
        typing_input(f'Are you sure you want to delete "{name}"? (y/n) 💊: ')
        .strip()
        .lower()
    )
    if confirmation == "y":
        book.delete(name)
        typing_output(f'Contact "{name}" has been deleted. ✅')
        save_contacts(book)
        return 0
    else:
        typing_output("Deletion cancelled. ⛔", color="yellow")
        print("")
        return 1


# ALL CONTACTS
@input_error
def all() -> Literal[1, 0]:
    """
    Display all contacts in the address book.

    Returns:
        int: 0 for success, 1 if no contacts found
    """
    if not book.data:
        typing_output(f"No records found")
        return 1

    print("")
    records = book.data.values()
    show_all_contacts_table(records)
    print("")

    return 0


# ==============
# === PHONE ===
# ==============


# ADD PHONE
@check_arguments(2)
@input_error
def add_phone(*args: tuple) -> Literal[1, 0]:
    """
    Add a phone number to an existing contact.

    Args:
        *args (tuple): Variable length argument list containing the name of the contact
                      and the phone number to add.

    Returns:
        int: 0 for success, 1 for failure
    """
    *name_parts, phone = args
    name = " ".join(name_parts)

    record = book.find_by_name(name)
    if record is None:
        no_record_message(name)
        typing_output(f"Cannot add phone. 🚫", style="yellow")
        return 1

    record.add_phone(phone)
    save_contacts(book)
    show_contact(record)  # show contact details in table
    return 0


# CHANGE PHONE
@check_arguments(3)
@input_error
def change_phone(*args: tuple) -> Literal[1, 0]:
    """
    Change an existing phone number for a contact.

    Args:
        *args (tuple): Variable length argument list containing the name of the contact,
                      the old phone number, and the new phone number.

    Returns:
        int: 0 for success, 1 for failure
    """
    *name_parts, old_phone, new_phone = args
    name = " ".join(name_parts)

    record = book.find_by_name(name)

    if record is None:
        no_record_message(name)
        typing_output(f"Cannot change phone. 🚫", style="yellow")
        return 1

    record.change_phone(old_phone, new_phone)
    save_contacts(book)

    typing_output(f"Contact updated ✅")
    show_contact(record)  # show contact details in table

    return 0


# SHOW PHONE
@check_arguments(1)
@input_error
def show_phone(*args: tuple) -> Literal[1, 0]:
    """
    Display all phone numbers for a specified contact.

    Args:
        *args (tuple): Variable length argument list containing the name of the contact.

    Returns:
        int: 0 for success, 1 for failure
    """
    name = " ".join(args)

    record = book.find_by_name(name)
    if record is None:
        no_record_message(name)
        typing_output(f"Cannot show phone. 🚫", style="yellow")
        return 1

    print("")
    typing_output(f"Phones of {name}:")
    print("")
    for phone in record.phones:
        typing_output(f" 📱 --> {phone}")
    print("")
    return 0


# DELETE PHONE
@check_arguments(2)
@input_error
def delete_phone(*args: tuple) -> Literal[1, 0]:
    """
    Delete a phone number from a specified contact.

    Args:
        *args (tuple): Variable length argument list containing the name of the contact
                    and the phone number to delete.

    Returns:
        int: 0 for success, 1 for failure
    """
    *name_parts, phone = args
    name = " ".join(name_parts)

    record = book.find_by_name(name)

    if not record:
        no_record_message(name)
        typing_output(f"Cannot delete phone. 🚫", style="yellow")
        return 1

    record.delete_phone(phone)
    save_contacts(book)

    typing_output(f"Phone {phone} deleted ✅")
    return 0


# ==============
# === EMAIL ===
# ==============


# ADD EMAIL
@check_arguments(2)
@input_error
def add_email(*args: tuple) -> Literal[1, 0]:
    """
    Add an email address to an existing contact.

    Args:
        *args (tuple): Variable length argument list containing the name of the contact
                    and the email to add.

    Returns:
        int: 0 for success, 1 for failure
    """
    *name_parts, email = args
    name = " ".join(name_parts)

    record = book.find_by_name(name)
    if not record:
        no_record_message(name)
        typing_output(f"Cannot add email. 🚫", style="yellow")
        return 1

    record.add_email(email)
    save_contacts(book)

    typing_output("Email added. ✅")
    return 0


@check_arguments(3)
@input_error
def change_email(*args: tuple) -> Literal[1, 0]:
    """
    Change an existing email address for a contact.

    Args:
        *args (tuple): Variable length argument list containing the name of the contact,
                    the old email, and the new email.

    Returns:
        int: 0 for success, 1 for failure
    """
    *name_parts, old_email, new_email = args
    name = " ".join(name_parts)

    record = book.find_by_name(name)
    if not record:
        no_record_message(name)
        typing_output(f"Cannot change email. 🚫", style="yellow")
        return 1

    try:
        record.change_email(old_email, new_email)
        save_contacts(book)
    except ValueError as e:
        console.print(str(e), style="red italic")
        return 1
    typing_output(f"Contact updated ✅")
    show_contact(record)
    return 0


@check_arguments(1)
@input_error
def show_email(*args: tuple) -> Literal[1, 0]:
    """
    Display all email addresses for a specified contact.

    Args:
        *args (tuple): Variable length argument list containing the name of the contact.

    Returns:
        int: 0 for success, 1 for failure
    """
    name = " ".join(args)

    record = book.find_by_name(name)
    if not record:
        typing_output(
            f'Error: Contact "{name}" not found. Cannot show emails. ⛔',
            color="yellow",
            s_style="italic",
        )
        return 1

    if not record.emails:
        typing_output(f"No emails found for {name}.", s_style="italic")
    else:
        typing_output(f"Emails of {name}:")
        for email in record.emails:
            print(" -", email.value)
    return 0


@check_arguments(2)
@input_error
def delete_email(*args: tuple) -> Literal[1, 0]:
    """
    Delete an email address from a specified contact.

    Args:
        *args (tuple): Variable length argument list containing the name of the contact
                    and the email to delete.

    Returns:
        int: 0 for success, 1 for failure
    """
    *name_parts, email = args
    name = " ".join(name_parts)

    record = book.find_by_name(name)
    if not record:
        no_record_message(name)
        typing_output("Cannot delete email. ⛔", color="yellow")
        return 1

    try:
        record.delete_email(email)
        save_contacts(book)

        typing_output(f'Email "{email}" for {name} deleted. ✅')
    except ValueError as e:
        console.print(str(e) + "🚨", style="red")
        return 1

    return 0


# =================
# === BIRTHDAY ===
# =================


# ADD BIRTHDAY
@check_arguments(2)
@input_error
def add_birthday(*args: tuple) -> Literal[1, 0]:
    """
    Add a birthday to an existing contact.

    Args:
        *args (tuple): Variable length argument list containing the name of the contact
                    and the birthday (in dd.mm.yyyy format) to add.

    Returns:
        int: 0 for success, 1 for failure
    """
    *name_parts, birthday = args
    name = " ".join(name_parts)

    record = book.find_by_name(name)

    if not record:
        no_record_message(name)
        typing_output("Cannot add birthday. ⛔", color="yellow")
        return 1

    record.add_birthday(birthday)
    save_contacts(book)

    typing_output(f"Birthday added for {name} ✅")
    typing_output(f"Birthday 🍰: {record.birthday.value}")
    return 0


# DELETE BIRTHDAY
@check_arguments(2)
@input_error
def delete_birthday(*args: tuple) -> Literal[1, 0]:
    """
    Delete a birthday from a specified contact.

    Args:
        *args (tuple): Variable length argument list containing the name of the contact
                    and the birthday to delete.

    Returns:
        int: 0 for success, 1 for failure
    """
    *name_parts, birthday = args
    name = " ".join(name_parts)

    record = book.find_by_name(name)

    if not record:
        no_record_message(name)
        typing_output("Cannot delete birthday. ⛔", color="yellow")
        return 1

    record.delete_birthday(birthday)

    return 0


# SHOW BIRTHDAY
@check_arguments(1)
@input_error
def show_birthday(*args: tuple) -> Literal[1, 0]:
    """
    Display the birthday for a specified contact.

    Args:
        *args (tuple): Variable length argument list containing the name of the contact.

    Returns:
        int: 0 for success, 1 for failure
    """
    name = " ".join(args)

    record = book.find_by_name(name)
    if not record:
        no_record_message(name)
        typing_output("Cannot show birthday. ⛔", color="yellow")
        return 1

    birthday = record.birthday
    typing_output(f"Birthday of {name} 🍰: {birthday}")

    return 0


# SHOW ALL BIRTHDAYS
@input_error
def all_birthdays() -> Literal[1, 0] | None:
    """
    Display all upcoming birthdays within a specified number of days.

    Prompts the user for the number of days to look ahead and displays
    any birthdays that will occur within that timeframe.

    Returns:
        int: 0 for success, 1 if no upcoming birthdays found
    """
    try:
        days = int(input("Enter a days number, in which to check? (int):"))
        if not days:
            days = 7
    except ValueError:
        console.print("Please enter a valid number of days.", style="yellow")
        return

    birthdays = book.get_birthday_in_days(days)
    day_word = "day" if days == 1 else "days"

    if not birthdays:
        console.print(
            f"No upcoming birthdays in the next {days} {day_word}", style="yellow"
        )
        return 1
    else:
        typing_output(f"Birthdays in the next {days} {day_word}: ")

        print("")
        show_birthdays_table(birthdays)  # show birthdays in table
        print("")

    return 0


# UPDATE BIRTHDAY
@check_arguments(2)
@input_error
def update_birthday(*args: tuple) -> Literal[1, 0]:
    """
    Update the birthday for an existing contact.

    Args:
        *args (tuple): Variable length argument list containing the name of the contact
                    and the new birthday (in dd.mm.yyyy format).

    Returns:
        int: 0 for success, 1 for failure
    """
    *name_parts, new_birthday = args
    name = " ".join(name_parts)

    record = book.find_by_name(name)

    if not record:
        no_record_message(name)
        typing_output("Cannot update birthday. ⛔", color="yellow")
        return 1

    record.add_birthday(new_birthday)
    save_contacts(book)

    typing_output(f"Birthday updated for {name} ✅")
    typing_output(f"New birthday 🍰: {record.birthday.value}")
    return 0


# =================
# === ADDRESS ===
# =================


# ADD ADDRESS
@check_arguments(2)
@input_error
def add_address(*args: tuple) -> Literal[1, 0]:
    """
    Add an address to an existing contact.

    Args:
        *args (tuple): Variable length argument list containing the name of the contact
                    and the address to add.

    Returns:
        int: 0 for success, 1 for failure
    """
    *name_parts, address = args
    name = " ".join(name_parts)

    record = book.find_by_name(name)

    if not record:
        no_record_message(name)
        typing_output("Cannot add address. ⛔", color="yellow")
        return 1

    record.add_address(address)
    save_contacts(book)

    typing_output(f"Address updated for {name} ✅")
    typing_output(f"New address: {record.address.value}")
    return 0


# UPDATE ADDRESS
@check_arguments(2)
@input_error
def update_address(*args: tuple) -> Literal[1, 0]:
    """
    Update the address for an existing contact.

    Args:
        *args (tuple): Variable length argument list containing the name of the contact
                    and the new address.

    Returns:
        int: 0 for success, 1 for failure
    """
    *name_parts, new_address = args
    name = " ".join(name_parts)

    record = book.find_by_name(name)

    if not record:
        no_record_message(name)
        typing_output("Cannot update address. ⛔", color="yellow")
        return 1

    record.add_address(new_address)
    save_contacts(book)

    typing_output(f"Address updated for {name} ✅")
    typing_output(f"New Address: {record.address.value}")
    return 0


def delete_address(*args: tuple) -> Literal[1, 0]:
    """
    Delete an address from a specified contact.

    Args:
        *args (tuple): Variable length argument list containing the name of the contact
                    and the address to delete.

    Returns:
        int: 0 for success, 1 for failure
    """
    *name_parts, address = args
    name = " ".join(name_parts)
    record = book.find_by_name(name)

    if not record:
        no_record_message(name)
        typing_output(f"Cannot delete address. ⛔", color="yellow")
        return 1

    record.delete_address(address)
    save_contacts(book)
    typing_output(f'Email "{address}" for {name} deleted. ✅')
    return 0


# ================
# === EXPORT ===
# ================


# EXPORT TO CSV
@input_error
def export_contacts_to_csv() -> None:
    """
    Export all contacts to a CSV file.

    Prompts the user for the directory path to save the CSV file and creates
    a file with the current date in the filename. Uses a default path if the
    user doesn't specify one.

    Returns:
        None
    """
    today = dtdt.now().strftime("%d.%m.%Y")
    filename = f"contacts_{today}.csv"

    STORAGE_DIR = Path(__file__).parent.parent / "storage"
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    default_path = STORAGE_DIR / filename

    dir_path = typing_input(
        f"Enter the path to save the CSV file (press Enter for default save) 🗄️: "
    ).strip()
    if dir_path:
        filepath = Path(dir_path) / filename
    else:
        filepath = default_path

    # Check if the directory exists
    if not filepath.parent.exists():
        typing_output(
            f"Error: The directory '{filepath.parent}' does not exist. 🚨", color="red"
        )

        create_dir = (
            input(
                f"Would you like to create the directory '{filepath.parent}'? (y/n): 💊"
            )
            .strip()
            .lower()
        )
        if create_dir == "y":
            filepath.parent.mkdir(parents=True, exist_ok=True)
            typing_output(f"Directory '{filepath.parent}' created. ✅", color="green")
        else:
            typing_output("Aborting export. ⛔", color="red")
            return

    # Check if the file is writable (optional, we just try opening it for writing)
    try:
        with filepath.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Phones", "Emails", "Birthday"])
            for record in book.data.values():
                writer.writerow(
                    [
                        record.name.value,
                        ", ".join(p.value for p in record.phones),
                        ", ".join(e.value for e in record.emails),
                        record.birthday.value if record.birthday else "",
                    ]
                )
        typing_output(f"Contacts saved to: {filepath} 💾")

    except (OSError, IOError) as e:
        console.print(f"Error writing to file: {e} 🚨 ", style="red")


@input_error
def edit_contact() -> None:
    """
    Edit details of an existing contact.

    Displays all contacts, prompts the user to select one, and then allows
    editing of different contact fields (email, phone, birthday, address).

    Returns:
        None
    """
    all()  # enumerate?
    name = input(
        "For whom do you want to change info? (name): "
    ).title()  # all names starts with Upper?
    record = book.find_by_name(name)
    if not record:
        typing_output(f"Contact {name} not found. ❗", color="yellow")
        return

    what_change = input(
        "What info do you want to change? (email, phone, birthday, address): "
    ).lower()

    if what_change == "email":
        emails = [email.value for email in record.emails]
        if not emails:
            typing_output("No email to edit for that contact. ❗", color="yellow")
            return

        for index, email in enumerate(emails, 1):
            typing_output(f"{index}. {email}")

        while True:
            email_index = input(
                "Enter the number of email you want to edit (or press Enter to cancel): "
            ).strip()
            if not email_index:
                typing_output("Email edit cancelled.", color="yellow")
                return

            if email_index.isdigit() and 1 <= int(email_index) <= len(emails):
                old_email = emails[int(email_index) - 1]
                new_email = input(f"Enter new value for email '{old_email}': ").strip()
                if not new_email:
                    typing_output("No changes were made to the email.", color="yellow")
                    return
                if not validate_email_str(new_email):
                    typing_output("Invalid email format.", color="red")
                    return
                change_email(name, old_email, new_email)
                break
            else:
                typing_output("Invalid index. Please try again.", color="yellow")

    elif what_change == "phone":
        phones = [phone.value for phone in record.phones]
        if not phones:
            typing_output("No phone to edit for that contact. ❗", color="yellow")
            return

        for index, phone in enumerate(phones, 1):
            typing_output(f"{index}. {phone}")

        while True:
            phone_index = input(
                "Enter the number of phone you want to edit (or press Enter to cancel): "
            ).strip()
            if not phone_index:
                typing_output("Phone edit cancelled.", color="yellow")
                return

            if phone_index.isdigit() and 1 <= int(phone_index) <= len(phones):
                old_phone = phones[int(phone_index) - 1]
                new_phone = input(f"Enter new value for phone '{old_phone}': ").strip()
                if not new_phone:
                    typing_output("No changes were made to the phone.", color="yellow")
                    return

                normalized_phone = validate_and_normalize_phone(new_phone)
                if not normalized_phone:
                    typing_output(f"Invalid phone number: {new_phone}. Phone must be exactly 10 digits 🚨", color="red")
                    return

                change_phone(name, old_phone, new_phone)
                break
            else:
                typing_output("Invalid index. Please try again.", color="yellow")

    elif what_change == "birthday":
        birthday = record.birthday
        if not birthday:
            typing_output(
                "This contact doesn't have a birthday set. Use 'expand contact' instead.",
                color="yellow",
            )
            return

        new_birthday = input(
            f"Enter new birthday (current: '{birthday}') or press Enter to cancel: "
        ).strip()
        if not new_birthday:
            typing_output("Birthday has not been changed.", color="yellow")
            return
        if not validate_date_str(new_birthday):
            typing_output("Invalid birthday format.", color="red")
            return
        update_birthday(name, new_birthday)
    elif what_change == "address":
        address = record.address
        if not address:
            typing_output(
                "This contact doesn't have a address set. Use 'expand contact' instead.",
                color="yellow",
            )
            return

        new_address = input(
            f"Enter new address (current: '{address}') or press Enter to cancel: "
        ).strip()
        if not new_address:
            typing_output("Address has not been changed.", color="yellow")
            return
        update_address(name, new_address)
    else:
        typing_output(
            f"Invalid option: {what_change}. Choose from: email, phone, birthday, address",
            color="yellow",
        )

@input_error
def expand_contact() -> None:
    """
    Expands a contact's information by adding additional details such as
    phone number, email, birthday, or address.

    Prompts the user to specify which parameter to add for a given contact.
    Checks if the contact exists in the contact book before proceeding.

    Returns:
        None
    """
    all()
    name = input("What contact do you want to expand? (name): ").title()
    record = book.find_by_name(name)
    if not record:
        typing_output(f"Contact {name} not found. ❗", color="yellow")
        return

    what_add = input(
        "Which parameter do you want to expand? (phone, email, birthday, address): "
    ).lower()

    if what_add == "phone":
        existing_phones = [phone.value for phone in record.phones]
        if existing_phones:
            typing_output(f"Contact '{name}' has these phone numbers:")
            for index, phone in enumerate(existing_phones, 1):
                typing_output(f"{index}. {phone}")

        phone = input(
            "Enter the phone number to add (or press Enter to cancel): "
        ).strip()
        if not phone:
            typing_output("No phone added.", color="yellow")
            return
        normalized_phone = validate_and_normalize_phone(phone)
        if not normalized_phone:
            typing_output(f"Invalid phone number: {phone}. Phone must be exactly 10 digits 🚨", color="red")
            return
        add_phone(name, phone)

    elif what_add == "email":
        existing_emails = [email.value for email in record.emails]
        if existing_emails:
            typing_output(f"Contact '{name}' has these emails:")
            for index, email in enumerate(existing_emails, 1):
                typing_output(f"{index}. {email}")

        email = input(
            "Enter the email address to add (or press Enter to cancel): "
        ).strip()
        if not email:
            typing_output("No email added.", color="yellow")
            return
        if not validate_email_str(email):
            typing_output("Invalid email format.", color="red")
            return
        add_email(name, email)
        typing_output(f"Email {email} added to {name} successfully. ✅", color="green")

    elif what_add == "birthday":
        if record.birthday:
            typing_output(f"Contact '{name}' already has a birthday: {record.birthday}")
            change = input("Do you want to change it? (y/n): ").lower()
            if change != "y":
                return

        birthday = input(
            "Enter birthday (dd.mm.yyyy) or press Enter to cancel: "
        ).strip()
        if not birthday:
            typing_output("No birthday added.", color="yellow")
            return
        if not validate_date_str(birthday):
            typing_output("Invalid birthday format.", color="red")
            return

        add_birthday(name, birthday)

    elif what_add == "address":
        if record.address:
            typing_output(f"Contact '{name}' already has a address: {record.address}")
            change = input("Do you want to change it? (y/n): ").lower()
            if change != "y":
                return
        address = input("Enter address to add (or press Enter to cancel): ").strip()
        if not address:
            typing_output("No address added.", color="yellow")
            return

        add_address(name, address)

    else:
        typing_output(
            f"Invalid option: {what_add}. Choose from: phone, email, birthday, address",
            color="yellow",
        )


@input_error
def delete_contact() -> None:
    """
    Deletes a contact or specific fields from a contact's information.

    Prompts the user to choose between deleting the entire contact or
    a specific field such as phone, email, birthday, or address.

    Returns:
        None
    """
    all()
    name = input("What contact do you want to modify? (name): ").title()
    record = book.find_by_name(name)
    if not record:
        typing_output(f"Contact {name} not found. ❗", color="yellow")
        return

    what_to_delete = input(
        "Do you want to delete the entire contact or just a field? (contact/field): "
    ).lower()

    if what_to_delete in ["contact", "c"]:
        confirm = input(f"Are you sure you want to delete {name}? (y/n): ").lower()
        if confirm == "y":
            book.delete(name)
            save_contacts(book)
            typing_output(f"Contact {name} has been deleted. ✅", color="green")
        else:
            typing_output("Deletion cancelled.", color="yellow")

    elif what_to_delete in ["field", "f"]:
        field = input(
            "Which field do you want to delete? (phone/email/birthday/address): "
        ).lower()

        if field == "phone":
            phones = [phone.value for phone in record.phones]
            if not phones:
                typing_output(f"Contact '{name}' has no phone numbers.", color="yellow")
                return

            typing_output(f"Contact '{name}' has these phone numbers:")
            for index, phone in enumerate(phones, 1):
                typing_output(f"{index}. {phone}")

            phone_index = input(
                "Enter the number of the phone to delete (or press Enter to cancel): "
            ).strip()
            if (
                not phone_index
                or not phone_index.isdigit()
                or int(phone_index) < 1
                or int(phone_index) > len(phones)
            ):
                typing_output("Invalid selection or cancelled.", color="yellow")
                return

            phone = phones[int(phone_index) - 1]
            delete_phone(name, phone)
            typing_output(f"Phone {phone} removed from {name}. ✅", color="green")

        elif field == "email":
            emails = [email.value for email in record.emails]
            if not emails:
                typing_output(
                    f"Contact '{name}' has no email addresses.", color="yellow"
                )
                return

            typing_output(f"Contact '{name}' has these emails:")
            for index, email in enumerate(emails, 1):
                typing_output(f"{index}. {email}")

            email_index = input(
                "Enter the number of the email to delete (or press Enter to cancel): "
            ).strip()
            if (
                not email_index
                or not email_index.isdigit()
                or int(email_index) < 1
                or int(email_index) > len(emails)
            ):
                typing_output("Invalid selection or cancelled.", color="yellow")
                return

            email = emails[int(email_index) - 1]
            delete_email(name, email)
            typing_output(f"Email {email} removed from {name}. ✅", color="green")

        elif field == "birthday":
            birthday = record.birthday
            if not birthday:
                typing_output(f"Contact '{name}' has no birthday.", color="yellow")
                return

            change = input("Do you want to delete birthday? (y/n): ").lower()
            if change != "y":
                typing_output("Birthday deletion cancelled.", color="yellow")
                return
            delete_birthday(name, birthday)
            typing_output(f"Birthday {birthday} deleted.", color="yellow")

        elif field == "address":
            address = record.address
            if not address:
                typing_output(
                    f"Contact '{name}' has no addresses to delete.", color="yellow"
                )
                return

            typing_output(f"Contact '{name}' has address: {address}")
            change = input("Do you want to delete address? (y/n): ").lower()
            if change != "y":
                typing_output("Address deletion canceled.", color="yellow")
                return
            delete_address(name, address)
            typing_output(f"Address {address} removed from {name}. ✅", color="green")

        else:
            typing_output(
                f"Invalid field: {field}. Choose from: phone, email, birthday, address",
                color="yellow",
            )

    else:
        typing_output(
            f"Invalid option: {what_to_delete}. Choose either 'contact' or 'field'",
            color="yellow",
        )


@input_error
def display_contact() -> None:
    """
    Displays the details of a contact selected by the user.

    Shows all available contacts and prompts the user to select one
    by entering its index. If an invalid or empty selection is made,
    the user is prompted again.

    Returns:
        None
    """
    if not book.data:
        typing_output("The contact book is empty ", color="yellow")
        return

    for index, name in enumerate(book.data.keys(), 1):
        typing_output(f"{index}. {name}")
    while True:
        what_contact = input("Enter number of contact you want to show (int): ")
        if not what_contact:
            typing_output(f"You did not choose any contact", color="yellow")
            try_again = input("Would you like to try again? (y/n): ").lower()
            if try_again != "y":
                print("Exiting contact selection.")
                return
        elif not what_contact.isdigit():  # Check if the input is not a number
            typing_output("Invalid input! Please enter a valid number.", color="yellow")
        else:
            selected_index = int(what_contact) - 1
            if 0 <= selected_index < len(book.data):
                selected_name = list(book.data.keys())[selected_index]
                show_contact(book.find_by_name(selected_name))
                break
            else:
                typing_output(
                    "Invalid contact number. Please select from the list",
                    color="yellow",
                )
                return
