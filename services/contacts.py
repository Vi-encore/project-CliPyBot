from colorama import Fore, Back, Style
from decorators.decorators import input_error, check_arguments
from models.contact import Record
from helpers.helpers import load_contacts, save_contacts

# ==== COMMANDS ====
book = load_contacts()
# 1 add
@check_arguments(2)
@input_error

def add(*args: tuple):
    *name_parts, phone = args
    name = " ".join(name_parts)
    
    record = book.find(name)
    message = "Contact updated."
    
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    print(message)
    save_contacts(book)
    return 0

# 2 change
@check_arguments(3)
@input_error

def change(*args: tuple):
    *name_parts, old_phone, new_phone = args
    name = " ".join(name_parts) 
    
    record = book.find(name)
    if record is None:
        raise ValueError(f'Contact {name} cannot be found')
    record.edit_phone(old_phone, new_phone)
    print(f'Contact updated')
    save_contacts(book)
    return 0

#3 phone
@check_arguments(1)
@input_error
def phone(*args: tuple):
    name = " ".join(args)
    
    record = book.find(name)
    if record is None:
        raise ValueError(f'Contact {name} cannot be found')
    else:
        print(f'Phone of {name}:')
        for phone in record.phones:
            print(phone)
    return 0

#4 all
@input_error
def all():
    
    if not book.data:
        print(f'No records found')
        return 1
    
    for record in book.data.values():
        print(Fore.GREEN + f'{record.name}:' + Style.RESET_ALL)
        for phone in record.phones:
            print(f'--tel:{phone}')
        if record.birthday:
            print(f'--birthday:{record.birthday}')
            
    return 0

# 5 add-birthday
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

# 6 show-birthday
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

# 7 birthdays
@input_error
def birthdays():
    birthdays = book.get_upcoming_birthdays()
    if not birthdays:
        print('No upcoming birthdays')
    else:
        for birthday in birthdays:
            print(f"{birthday['name']} has birthday on {birthday['congratulation_date']}")
    return 0

@check_arguments(1)
@input_error

def remove(*args:tuple):
    name = " ".join(args)
    
    record = book.find(name)
    
    if not record:
        print(f'Contact with name: {name} is not found')
    else: 
        book.delete(name)
        print(f'Contact with name {name} is deleted')
        save_contacts(book)
    
    return 0
    
def close():
    save_contacts(book)
    print(Back.LIGHTWHITE_EX + Fore.BLACK + 'Goodbye. Data saved' + Style.RESET_ALL)
    return 0