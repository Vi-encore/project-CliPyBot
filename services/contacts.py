from colorama import Fore, Back, Style
from decorators.decorators import input_error, check_arguments
from models.contact import Record
from helpers.helpers import load_contacts, save_contacts

book = load_contacts()

# ADD NEW CONTACT
@input_error
def add():
    name = input("Contact name: ").strip()
    if not name:
        print(Fore.RED + "Name is required to create a contact." + Style.RESET_ALL)
        return 1

    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
        print(Fore.GREEN + "New contact created." + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "Contact already exists. Updating details..." + Style.RESET_ALL)

    # Loop for phone
    while True:
        phone = input("Contact phone (press Enter to skip): ").strip()
        if not phone:
            break
        try:
            record.add_phone(phone)
            break
        except Exception as e:
            print(Fore.RED + "Invalid phone. Please try again." + Style.RESET_ALL)

    # Loop for email
    while True:
        email = input("Contact email (press Enter to skip): ").strip()
        if not email:
            break
        try:
            record.add_email(email)
            break
        except Exception as e:
            print(Fore.RED + "Invalid email. Please try again." + Style.RESET_ALL)

    # Loop for birthday
    while True:
        birthday = input("Contact birthday (dd.mm.yyyy, press Enter to skip): ").strip()
        if not birthday:
            break
        try:
            record.add_birthday(birthday)
            break
        except Exception as e:
            print(Fore.RED + "Invalid birthday. Please use format dd.mm.yyyy." + Style.RESET_ALL)

    save_contacts(book)

    print(Fore.GREEN + f'Contact "{name}" saved successfully.' + Style.RESET_ALL)
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
    print(Back.LIGHTWHITE_EX + Fore.BLACK + 'Goodbye. Data saved' + Style.RESET_ALL)
    return 0