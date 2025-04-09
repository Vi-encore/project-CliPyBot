import csv
from pathlib import Path
from datetime import datetime as dtdt
from decorators.decorators import input_error, check_arguments
from models.contact import Record
from helpers.helpers import save_contacts
from rich.console import Console
from helpers.create_table import show_contact_in_table, show_all_contacts_table, show_birthdays_table
from helpers.typing_effect import typing_output, typing_input
from data.state import book

console = Console()

def no_record_message(name):
    typing_output(f'Contact "{name}" not found.❗', color="yellow")
    return

def show_contact(record):
    print('')
    show_contact_in_table(record)
    print('')
    return

#===============
# === RECORD ===
#===============

# ADD NEW CONTACT
@input_error
def add():
    name = typing_input("Contact name: (str): ")
    if not name:
        console.print("Name is required to create a contact. ❗", style="red") 
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
        birthday = typing_input("Contact birthday (dd.mm.yyyy, press Enter to skip): (str) ").strip()
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
    show_contact(record) # show contact details in table
    return 0

# FIND CONTACT
@check_arguments(1)
@input_error
def find(*args: tuple):
    name = " ".join(args)
    record = book.find(name)

    if not record:
        no_record_message(name)
        return 1

    typing_output("Contact found:")
    show_contact(record) # show contact details in table
    return 0

# REMOVE CONTACT
@check_arguments(1)
@input_error
def remove(*args: tuple):
    name = " ".join(args)

    record = book.find(name)

    if not record:
        no_record_message(name)
        typing_output(f'Cannot delete contact. 🚫', color="yellow")
        return 1

    typing_output( "Contact found:")
    show_contact(record) # show contact details in table

    confirmation = typing_input(f'Are you sure you want to delete "{name}"? (y/n) 💊: ').strip().lower()
    if confirmation == 'y':
        book.delete(name)
        typing_output(f'Contact "{name}" has been deleted. ✅' )
        save_contacts(book)
        return 0
    else:
        typing_output("Deletion cancelled. ⛔", color="yellow")
        print('')
        return 1

# ALL CONTACTS
@input_error
def all():
    if not book.data:
        typing_output(f'No records found')
        return 1
    
    print('')
    records = book.data.values()
    show_all_contacts_table(records)
    print('')
    
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
        no_record_message(name)
        typing_output(f'Cannot add phone. 🚫', style="yellow")
        return 1
    
    record.add_phone(phone)
    save_contacts(book)
    typing_output(f'Phone added ✅')
    show_contact(record) # show contact details in table
    return 0

# CHANGE PHONE
@check_arguments(3)
@input_error
def change_phone(*args: tuple):
    *name_parts, old_phone, new_phone = args
    name = " ".join(name_parts) 
    
    record = book.find(name)
    
    if record is None:
        no_record_message(name)
        typing_output(f'Cannot change phone. 🚫', style="yellow")
        return 1
    
    record.change_phone(old_phone, new_phone)
    save_contacts(book)
    
    typing_output(f'Contact updated ✅')
    show_contact(record) # show contact details in table
    
    return 0

# SHOW PHONE
@check_arguments(1)
@input_error
def show_phone(*args: tuple):
    name = " ".join(args)
    
    record = book.find(name)
    if record is None:
        no_record_message(name)
        typing_output(f'Cannot show phone. 🚫', style="yellow")
        return 1
    
    print('')
    typing_output(f'Phones of {name}:')
    print('')
    for phone in record.phones:
        typing_output( f" 📱 --> {phone}")
    print('')
    return 0

# DELETE PHONE
@check_arguments(2)
@input_error
def delete_phone(*args: tuple):
    *name_parts, phone = args
    name = " ".join(name_parts)
    
    record = book.find(name)

    if not record:
        no_record_message(name)
        typing_output(f'Cannot delete phone. 🚫', style="yellow")
        return 1
    
    record.delete_phone(phone)
    save_contacts(book)

    typing_output(f'Phone {phone} deleted ✅')
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
        no_record_message(name)
        typing_output(f'Cannot add email. 🚫', style="yellow")
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

    record = book.find(name)
    if not record:
        no_record_message(name)
        typing_output(f'Cannot change email. 🚫', style="yellow")
        return 1

    try:
        record.change_email(old_email, new_email)
        print(f'Email changed for {name}')
        save_contacts(book)
    except ValueError as e:
        console.print(str(e), style="red italic")
        return 1
    return 0

@check_arguments(1)
@input_error
def show_email(*args: tuple):
    name = " ".join(args)

    record = book.find(name)
    if not record:
        typing_output(f'Error: Contact \"{name}\" not found. Cannot show emails. ⛔', color="yellow", s_style="italic")
        return 1

    if not record.emails:
        typing_output(f'No emails found for {name}.', s_style="italic")
    else:
        typing_output(f'Emails of {name}:')
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
        no_record_message(name)
        typing_output('Cannot delete email. ⛔', color="yellow")
        return 1

    try:
        record.delete_email(email)
        save_contacts(book)
        
        typing_output(f'Email "{email}" for {name} deleted. ✅')
    except ValueError as e:
        console.print(str(e) + "🚨", style="red")
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
        no_record_message(name)
        typing_output('Cannot add birthday. ⛔', color="yellow")
        return 1
    
    record.add_birthday(birthday)
    save_contacts(book)
    
    typing_output(f'Birthday added for {name} ✅')
    typing_output(f'Birthday 🍰: {record.birthday.value}')
    return 0

# SHOW BIRTHDAY
@check_arguments(1)
@input_error
def show_birthday(*args:tuple):
    name = " ".join(args) 
    
    record = book.find(name)
    if not record:
        no_record_message(name)
        typing_output('Cannot show birthday. ⛔', color="yellow")
        return 1
    
    birthday = record.birthday
    typing_output(f'Birthday of {name} 🍰: {birthday}')
            
    return 0

# SHOW ALL BIRTHDAYS
@input_error
def all_birthdays():
    birthdays = book.get_upcoming_birthdays()
    if not birthdays:
        print('No upcoming birthdays')
    else:
        print('')
        show_birthdays_table(birthdays)
        print('')
    return 0
    
@check_arguments(2)
@input_error
def update_birthday(*args:tuple):
    *name_parts, new_birthday = args
    name = " ".join(name_parts) 
    
    record = book.find(name)
    
    if not record:
        no_record_message(name)
        typing_output('Cannot update birthday. ⛔', color="yellow")
        return 1
    
    record.add_birthday(new_birthday)
    save_contacts(book)
    
    typing_output(f'Birthday updated for {name} ✅')
    typing_output(f'New birthday 🍰: {record.birthday.value}')
    return 0

#================
# === EXPORT ===
#================

# EXPORT TO CSV
@input_error
def export_contacts_to_csv():
    today = dtdt.now().strftime("%d.%m.%Y")
    filename = f"contacts_{today}.csv"
    
    STORAGE_DIR = Path(__file__).parent.parent / "storage"
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    
    default_path = STORAGE_DIR / filename
    
    dir_path = typing_input(f"Enter the path to save the CSV file (press Enter for default save) 🗄️: ").strip()
    if dir_path:
        filepath = Path(dir_path) / filename
    else:
        filepath = default_path

    # Check if the directory exists
    if not filepath.parent.exists():
        typing_output(f"Error: The directory '{filepath.parent}' does not exist. 🚨", color="red")
        
        create_dir = input(f"Would you like to create the directory '{filepath.parent}'? (y/n): 💊").strip().lower()
        if create_dir == 'y':
            filepath.parent.mkdir(parents=True, exist_ok=True)
            typing_output(f"Directory '{filepath.parent}' created. ✅", color="green")
        else:
            typing_output("Aborting export. ⛔", color="red")
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
        typing_output(f"Contacts saved to: {filepath} 💾" )
    
    except (OSError, IOError) as e:
        console.print(f"Error writing to file: {e} 🚨 ", style="red")
