import csv
from pathlib import Path
import datetime as dt
from datetime import datetime as dtdt
from decorators.decorators import input_error, check_arguments
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


def no_record_message(name):
    typing_output(f'Contact "{name}" not found.❗', color="yellow")
    return


def show_contact(record):
    print("")
    show_contact_in_table(record)
    print("")
    return


# ===============
# === RECORD ===
# ===============


# ADD NEW CONTACT
@input_error
def add():
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

    save_contacts(book)

    typing_output(f'Contact "{name}" saved successfully. ✅', color="green")
    show_contact(record)  # show contact details in table
    return 0


# FIND CONTACT
@input_error
def find():
    print('')
    show_options_for_query()
    print('')
    
    # Loop for query
    while True:
        query = typing_input("How do you want to search (Enter the number of field): (num) ").strip().lower()
        
        if not query:
            typing_output("No input provided❗", color="yellow")
            typing_output("You can enter any other command")
            return 1
        
        if query not in ["1", "2", "3", "4"]:
            typing_output("Invalid option. Please enter a number between 1 and 4. ❗", color="yellow")
            continue
        break
    
    # Get args based on query
    if query == "1": # search by name
        args = typing_input("Enter the name of the contact: (str): ").strip().split() 
    elif query == "2":
        args = typing_input("Enter the phone number: (num): ").strip().split()
    elif query == "3":
        args = typing_input("Enter the email address: (str): ").strip().split()
    elif query == "4":
        args = typing_input("Enter the birthday (dd.mm.yyyy): (str): ").strip().split()
    else:
        typing_output("Invalid option. Please enter a number between 1 and 4. ❗", color="yellow")
        return 1
    if not args:
        typing_output("No input provided. Please enter a valid query. ❗", color="yellow")
        return 1
    
    # Call the find method with the appropriate arguments
    if query == "1": # search by name
        result = book.find(" ".join(args), by_name=True)
    elif query == "2": # search by phone
        result = book.find(" ".join(args), by_phone=True)
    elif query == "3": # search by email
        result = book.find(" ".join(args), by_email=True)
    elif query == "4": # search by birthday
        result = book.find(" ".join(args), by_birthday=True)
    else:
        typing_output("Invalid option. Please enter a number between 1 and 4. ❗", color="yellow")
        return 1
    
    if not result:
        typing_output("No record found. ❗", color="yellow")
        return 1
    # If a record is found, show the contact details
    
    print('')
    typing_output("Contact found:")
    show_all_contacts_table(result) # show contacts details in table
    print('')
    return 0

# REMOVE CONTACT
@check_arguments(1)
@input_error
def remove(*args: tuple):
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
def all():
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
def add_phone(*args: tuple):
    *name_parts, phone = args
    name = " ".join(name_parts)

    record = book.find_by_name(name)
    if record is None:
        no_record_message(name)
        typing_output(f"Cannot add phone. 🚫", style="yellow")
        return 1

    record.add_phone(phone)
    save_contacts(book)
    typing_output(f"Phone added ✅")
    show_contact(record)  # show contact details in table
    return 0


# CHANGE PHONE
@check_arguments(3)
@input_error
def change_phone(*args: tuple):
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
def show_phone(*args: tuple):
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
def delete_phone(*args: tuple):
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
def add_email(*args: tuple):
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
def change_email(*args: tuple):
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
def show_email(*args: tuple):
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
def delete_email(*args: tuple):
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
def add_birthday(*args: tuple):
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


# SHOW BIRTHDAY
@check_arguments(1)
@input_error
def show_birthday(*args: tuple):
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
def all_birthdays(*args):
    try:
        days = int(args[0]) if args else 7
    except ValueError:
        console.print("Please enter a valid number of days.", style="yellow")
        return
    
    birthdays = book.get_birthday_in_days(days)
    today = dt.date.today()
    day_word = "day" if days == 1 else "days"

    if not birthdays:
        console.print(f"No upcoming birthdays in the next {days} {day_word}", style="yellow")
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
def update_birthday(*args: tuple):
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


# ================
# === EXPORT ===
# ================


# EXPORT TO CSV
@input_error
def export_contacts_to_csv():
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


def edit_contact():
    all()
    name = input("For whom do you want to change info? (name): ").title()
    record = book.find_by_name(name)
    if not record:
        typing_output(f"Contact {name} not found. ❗", color="yellow")
        return

    what_change = input("What info do you want to change? (email, phone, birthday): ").lower()

    if what_change == "email":
        emails = [email.value for email in record.emails]
        if not emails:
            typing_output('No email to edit for that contact. ❗', color="yellow")
            return

        for index, email in enumerate(emails, 1):
            typing_output(f"{index}. {email}")

        while True:
            email_index = input("Enter the number of email you want to edit (or press Enter to cancel): ").strip()
            if not email_index:
                typing_output("Email edit cancelled.", color="yellow")
                return

            if email_index.isdigit() and 1 <= int(email_index) <= len(emails):
                old_email = emails[int(email_index) - 1]
                new_email = input(f"Enter new value for email '{old_email}': ").strip()
                if not new_email:
                    typing_output("No changes were made to the email.", color="yellow")
                    return

                change_email(name, old_email, new_email)
                break
            else:
                typing_output("Invalid index. Please try again.", color="yellow")

    elif what_change == "phone":
        phones = [phone.value for phone in record.phones]
        if not phones:
            typing_output('No phone to edit for that contact. ❗', color="yellow")
            return

        for index, phone in enumerate(phones, 1):
            typing_output(f"{index}. {phone}")

        while True:
            phone_index = input("Enter the number of phone you want to edit (or press Enter to cancel): ").strip()
            if not phone_index:
                typing_output("Phone edit cancelled.", color="yellow")
                return

            if phone_index.isdigit() and 1 <= int(phone_index) <= len(phones):
                old_phone = phones[int(phone_index) - 1]
                new_phone = input(f"Enter new value for phone '{old_phone}': ").strip()
                if not new_phone:
                    typing_output("No changes were made to the phone.", color="yellow")
                    return

                change_phone(name, old_phone, new_phone)
                break
            else:
                typing_output("Invalid index. Please try again.", color="yellow")

    elif what_change == "birthday":
        birthday = record.birthday
        if not birthday:
            typing_output("This contact doesn't have a birthday set. Use 'expand contact' instead.", color="yellow")
            return

        new_birthday = input(f"Enter new birthday (current: '{birthday}') or press Enter to cancel: ").strip()
        if not new_birthday:
            typing_output("Birthday has not been changed.", color="yellow")
            return

        update_birthday(name, new_birthday)

    else:
        typing_output(f"Invalid option: {what_change}. Choose from: email, phone, birthday", color="yellow")


def expand_contact():
    all()
    name = input("What contact do you want to expand? (name): ").title()
    record = book.find_by_name(name)
    if not record:
        typing_output(f"Contact {name} not found. ❗", color="yellow")
        return

    what_add = input("Which parameter do you want to expand? (phone, email, birthday): ").lower()

    if what_add == "phone":
        existing_phones = [phone.value for phone in record.phones]
        if existing_phones:
            typing_output(f"Contact '{name}' has these phone numbers:")
            for index, phone in enumerate(existing_phones, 1):
                typing_output(f"{index}. {phone}")

        phone = input("Enter the phone number to add (or press Enter to cancel): ").strip()
        if not phone:
            typing_output("No phone added.", color="yellow")
            return

        add_phone(name, phone)
        typing_output(f"Phone {phone} added to {name} successfully. ✅", color="green")

    elif what_add == "email":
        existing_emails = [email.value for email in record.emails]
        if existing_emails:
            typing_output(f"Contact '{name}' has these emails:")
            for index, email in enumerate(existing_emails, 1):
                typing_output(f"{index}. {email}")

        email = input("Enter the email address to add (or press Enter to cancel): ").strip()
        if not email:
            typing_output("No email added.", color="yellow")
            return

        add_email(name, email)
        typing_output(f"Email {email} added to {name} successfully. ✅", color="green")

    elif what_add == "birthday":
        if record.birthday:
            typing_output(f"Contact '{name}' already has a birthday: {record.birthday}")
            change = input("Do you want to change it? (y/n): ").lower()
            if change != "y":
                return

        birthday = input("Enter birthday (dd.mm.yyyy) or press Enter to cancel: ").strip()
        if not birthday:
            typing_output("No birthday added.", color="yellow")
            return

        add_birthday(name, birthday)
        typing_output(f"Birthday added to {name} successfully. ✅", color="green")

    else:
        typing_output(f"Invalid option: {what_add}. Choose from: phone, email, birthday", color="yellow")


def delete_contact():
    all()
    name = input("What contact do you want to modify? (name): ").title()
    record = book.find_by_name(name)
    if not record:
        typing_output(f"Contact {name} not found. ❗", color="yellow")
        return

    what_to_delete = input("Do you want to delete the entire contact or just a field? (contact/field): ").lower()

    if what_to_delete in ["contact", "c"]:
        confirm = input(f"Are you sure you want to delete {name}? (y/n): ").lower()
        if confirm == "y":
            book.delete(name)
            save_contacts(book)
            typing_output(f"Contact {name} has been deleted. ✅", color="green")
        else:
            typing_output("Deletion cancelled.", color="yellow")

    elif what_to_delete in ["field", "f"]:
        field = input("Which field do you want to delete? (phone/email): ").lower()

        if field == "phone":
            phones = [phone.value for phone in record.phones]
            if not phones:
                typing_output(f"Contact '{name}' has no phone numbers.", color="yellow")
                return

            typing_output(f"Contact '{name}' has these phone numbers:")
            for index, phone in enumerate(phones, 1):
                typing_output(f"{index}. {phone}")

            phone_index = input("Enter the number of the phone to delete (or press Enter to cancel): ").strip()
            if not phone_index or not phone_index.isdigit() or int(phone_index) < 1 or int(phone_index) > len(phones):
                typing_output("Invalid selection or cancelled.", color="yellow")
                return

            phone = phones[int(phone_index) - 1]
            delete_phone(name, phone)
            save_contacts(book)
            typing_output(f"Phone {phone} removed from {name}. ✅", color="green")

        elif field == "email":
            emails = [email.value for email in record.emails]
            if not emails:
                typing_output(f"Contact '{name}' has no email addresses.", color="yellow")
                return

            typing_output(f"Contact '{name}' has these emails:")
            for index, email in enumerate(emails, 1):
                typing_output(f"{index}. {email}")

            email_index = input("Enter the number of the email to delete (or press Enter to cancel): ").strip()
            if not email_index or not email_index.isdigit() or int(email_index) < 1 or int(email_index) > len(emails):
                typing_output("Invalid selection or cancelled.", color="yellow")
                return

            email = emails[int(email_index) - 1]
            delete_email(name, email)
            save_contacts(book)
            typing_output(f"Email {email} removed from {name}. ✅", color="green")

        else:
            typing_output(f"Invalid field: {field}. Choose from: phone, email", color="yellow")

    else:
        typing_output(f"Invalid option: {what_to_delete}. Choose either 'contact' or 'field'", color="yellow")