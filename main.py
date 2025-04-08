from colorama import Fore, Back, Style
from services import contacts
from helpers.helpers import parse_input

def main():
    '''
        Main function for the assistant bot
        takes following commands:add
        - hello - greets the user
        - add <name> <phone> - adds a contact
        - change <name> <old_phone> <new_phone> - replace phone number 
        - phone <name> - shows all phones of a contact
        - all - shows all contacts
        - add-birthday <name> <birthday>- add birthday to the contact
        - show-birthday <name> - show birthday date of the contact
        - birthdays - show all upcoming birthdays for the next week (workdays)
        - close/exit - closes the bot
    '''
    print( Back.LIGHTWHITE_EX + Fore.BLACK + "Welcome to the assistant bot!" + Style.RESET_ALL)
    print('')
    while True:
        user_input = input(Fore.BLUE + 'Enter a command: ' + Style.RESET_ALL)
        if user_input.strip() == '':
            print(Fore.YELLOW + 'Please enter a command.')
            continue
        
        cmd, *args = parse_input(user_input)
        
        if cmd == '':
            print(Fore.YELLOW + 'Please enter a command.')
            continue
        elif cmd in ["close", "exit"]:
            contacts.close()
            break
        elif cmd == 'hello':
            print(Fore.GREEN + 'Hello! I am your assistant, how can I help you?' + Style.RESET_ALL)
        elif cmd == 'add':
            contacts.add(*args)
        elif cmd == 'remove':
            contacts.remove(*args)
        elif cmd == 'change':
            contacts.change(*args)
        elif cmd == 'phone':
            contacts.phone(*args)
        elif cmd == 'all':
            contacts.all()
        elif cmd == 'add-birthday':
            contacts.add_birthday(*args)
        elif cmd == 'show-birthday':
            contacts.show_birthday(*args)
        elif cmd == 'birthdays':
            contacts.birthdays()
        else:
            print(Fore.YELLOW + 'Unknown command. Please try again.')
         
if __name__ == '__main__':
    main()