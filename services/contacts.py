import csv
from pathlib import Path
from datetime import datetime as dtdt
from colorama import Fore, Back, Style
from decorators.decorators import input_error, check_arguments
from models.contact import Record
from helpers.helpers import load_contacts, save_contacts
from rich.console import Console
from rich.table import Table
from rich import box
from helpers.helpers import typing_input, typing_output

console = Console()

book = load_contacts()

# ADD NEW CONTACT
@input_error
def add():
    name = typing_input("Contact name: (str): ")
    if not name:
        console.print("Name is required to create a contact. ❗⚠️ ", style="red italic") 
        return 1

    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
        typing_output( "New contact created.")
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
            console.print("Invalid phone. ❗⚠️ ", style="red italic")
            typing_output("Please try again. ", color="yellow", s_style="italic")

    # Loop for email
    while True:
        email = typing_input("Contact email (press Enter to skip): (str): ").strip()
        if not email:
            break
        try:
            record.add_email(email)
            break
        except Exception as e:
            console.print("Invalid email ❗⚠️ ", style="red italic")
            typing_output("Please try again. ", color="yellow", s_style="italic")

    # Loop for birthday
    while True:
        birthday = typing_input("Contact birthday (dd.mm.yyyy, press Enter to skip): (str) ").strip()
        if not birthday:
            break
        try:
            record.add_birthday(birthday)
            break
        except Exception as e:
            console.print("Invalid birthday format.❗⚠️ ", style="red italic")
            typing_output("Please use the format dd.mm.yyyy. ", color="yellow", s_style="italic")

    save_contacts(book)

    typing_output(f'Contact "{name}" saved successfully.')
    print("Contact details:")
    print(record)
    return 0

# REMOVE CONTACT
@check_arguments(1)
@input_error
def remove(*args: tuple):
    name = " ".join(args)

    record = book.find(name)

    if not record:
        print(Fore.RED + f'Contact "{name}" not found.' + Style.RESET_ALL)
        return 1

    print(Fore.YELLOW + "Contact found:" + Style.RESET_ALL)
    print(record)  # shows all details (phones, emails, birthday, etc.)

    confirmation = input(f'Are you sure you want to delete "{name}"? (y/n): ').strip().lower()
    if confirmation == 'y':
        book.delete(name)
        print(Fore.GREEN + f'Contact "{name}" has been deleted.' + Style.RESET_ALL)
        save_contacts(book)
        return 0
    else:
        print(Fore.YELLOW + "Deletion cancelled." + Style.RESET_ALL)
        return 1

# ALL CONTACTS
@input_error
def all():
    if not book.data:
        print(f'No records found')
        return 1
    
    for record in book.data.values():
        print(Fore.GREEN + f'{record.name}:' + Style.RESET_ALL)
        for phone in record.phones:
            print(f'--tel:{phone}')
        for email in record.emails:
            print(f'--email:{email}')
        if record.birthday:
            print(f'--birthday:{record.birthday}')

    return 0

#==============
# === PHONE ===
#==============

# ADD PHONE
@check_arguments(2)
@input_error
def add_phone(*args: tuple):
    *name_parts, phone = args
    name = " ".join(name_parts)
    
    record = book.find(name)
    if record is None:
        raise ValueError(f'Contact {name} cannot be found')
    
    record.add_phone(phone)
    print(f'Phone added')
    save_contacts(book)
    return 0

# CHANGE PHONE
@check_arguments(3)
@input_error
def change_phone(*args: tuple):
    *name_parts, old_phone, new_phone = args
    name = " ".join(name_parts) 
    
    record = book.find(name)
    
    if record is None:
        raise ValueError(f'Contact {name} cannot be found')
    
    record.change_phone(old_phone, new_phone)
    print(f'Contact updated')
    
    save_contacts(book)
    return 0

# SHOW PHONE
@check_arguments(1)
@input_error
def show_phone(*args: tuple):
    name = " ".join(args)
    
    record = book.find(name)
    if record is None:
        raise ValueError(f'Contact {name} cannot be found')
    else:
        print(f'Phone of {name}:')
        for phone in record.phones:
            print(phone)
    return 0

# DELETE PHONE
@check_arguments(2)
@input_error
def delete_phone(*args: tuple):
    *name_parts, phone = args
    name = " ".join(name_parts)
    
    record = book.find(name)
    if record is None:
        raise ValueError(f'Contact {name} cannot be found')
    else:
        record.delete_phone(phone)
        print(f'Phone {phone} deleted')
        save_contacts(book)

    return 0

#==============
# === EMAIL ===
#==============

# ADD EMAIL
@check_arguments(2)
@input_error
def add_email(*args: tuple):
    *name_parts, email = args
    name = " ".join(name_parts)

    record = book.find(name)
    if not record:
        print(Fore.RED + f'Error: Contact "{name}" not found. Cannot add email.' + Style.RESET_ALL)
        return 1

    record.add_email(email)
    print("Email added.")
    save_contacts(book)
    return 0

@check_arguments(3)
@input_error
def change_email(*args: tuple):
    *name_parts, old_email, new_email = args
    name = " ".join(name_parts)

    record = book.find(name)
    if not record:
        print(Fore.RED + f'Error: Contact "{name}" not found. Cannot change email.' + Style.RESET_ALL)
        return 1

    try:
        record.change_email(old_email, new_email)
        print(f'Email changed for {name}')
        save_contacts(book)
    except ValueError as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
        return 1
    return 0

@check_arguments(1)
@input_error
def show_email(*args: tuple):
    name = " ".join(args)

    record = book.find(name)
    if not record:
        print(Fore.RED + f'Error: Contact \"{name}\" not found. Cannot show emails.' + Style.RESET_ALL)
        return 1

    if not record.emails:
        print(Fore.YELLOW + f'No emails found for {name}.' + Style.RESET_ALL)
    else:
        print(f'Emails of {name}:')
        for email in record.emails:
            print(" -", email.value)
    return 0

@check_arguments(2)
@input_error
def delete_email(*args: tuple):
    *name_parts, email = args
    name = " ".join(name_parts)

    record = book.find(name)
    if not record:
        print(Fore.RED + f'Error: Contact \"{name}\" not found. Cannot delete email.' + Style.RESET_ALL)
        return 1

    try:
        record.delete_email(email)
        print(f'Email "{email}" for {name} deleted.')
        save_contacts(book)
    except ValueError as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
        return 1

    return 0

#=================
# === BIRTHDAY === 
#=================

# ADD BIRTHDAY
@check_arguments(2)
@input_error
def add_birthday(*args:tuple):
    *name_parts, birthday = args
    name = " ".join(name_parts) 
    
    record = book.find(name)
    
    if not record:
        print(Fore.RED + f'Error: Contact "{name}" not found. Cannot add birthday.' + Style.RESET_ALL)
        return 1
    
    record.add_birthday(birthday)
    print(f'Birthday added')

    save_contacts(book)
    return 0

# SHOW BIRTHDAY
@check_arguments(1)
@input_error
def show_birthday(*args:tuple):
    name = " ".join(args) 
    
    record = book.find(name)
    if not record:
        print(f'Record {name} is not found')
        return 1
    birthday = record.birthday
    print(f'Birthday of {name}: {birthday}')
            
    return 0

# SHOW ALL BIRTHDAYS
@input_error
def all_birthdays():
    birthdays = book.get_upcoming_birthdays()
    if not birthdays:
        print('No upcoming birthdays')
    else:
        for birthday in birthdays:
            print(f"{birthday['name']} has birthday on {birthday['congratulation_date']}")
    return 0
    
@check_arguments(2)
@input_error
def update_birthday(*args:tuple):
    *name_parts, new_birthday = args
    name = " ".join(name_parts) 
    
    record = book.find(name)
    
    if not record:
        print(Fore.RED + f'Error: Contact "{name}" not found. Cannot update birthday.' + Style.RESET_ALL)
        return 1
    
    record.add_birthday(new_birthday)
    print(f'Birthday updated')

    save_contacts(book)
    return 0
    
# CLOSE
def close():
    save_contacts(book)
    typing_output('Goodbye 🐇')
    typing_output('All data saved! 💾')
    return 0

# EXPORT TO CSV
@input_error
def export_contacts_to_csv():
    today = dtdt.now().strftime("%d.%m.%Y")
    filename = f"contacts_{today}.csv"
    
    STORAGE_DIR = Path(__file__).parent.parent / "storage"
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    
    default_path = STORAGE_DIR / filename
    
    dir_path = input(f"Enter the path to save the CSV file (press Enter for default save): ").strip()
    if dir_path:
        filepath = Path(dir_path) / filename
    else:
        filepath = default_path

    # Check if the directory exists
    if not filepath.parent.exists():
        print(Fore.RED + f"Error: The directory '{filepath.parent}' does not exist." + Style.RESET_ALL)
        create_dir = input(f"Would you like to create the directory '{filepath.parent}'? (y/n): ").strip().lower()
        if create_dir == 'y':
            filepath.parent.mkdir(parents=True, exist_ok=True)
            print(f"Directory '{filepath.parent}' created.")
        else:
            print("Aborting export.")
            return

    # Check if the file is writable (optional, we just try opening it for writing)
    try:
        with filepath.open('w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name', 'Phones', 'Emails', 'Birthday'])
            for record in book.data.values():
                writer.writerow([
                    record.name.value,
                    ', '.join(p.value for p in record.phones),
                    ', '.join(e.value for e in record.emails),
                    record.birthday.value if record.birthday else ''
                ])
        print(Fore.GREEN + f"Contacts saved to: {filepath}" + Style.RESET_ALL)
    
    except (OSError, IOError) as e:
        print(Fore.RED + f"Error writing to file: {e}" + Style.RESET_ALL)
