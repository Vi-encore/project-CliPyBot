from services import contacts
from helpers.helpers import parse_input, show_help, typing_output, typing_input
from rich.console import Console
from colorama import Fore, Style

# Initialize Console for rich output
console = Console()
   
def main():
    '''
        Main function for the assistant bot
        that works with contacts and notes.
    '''
    typing_output("⚡ Welcome to the Assistant Bot ⚡")
    typing_output("Loading... Please wait...")
    print('')


    while True:
        user_input = typing_input('Enter a command </>: ')
        if user_input.strip() == '':
            console.print('No command entered ⚠️', style='red bold')
            typing_output('Please enter a command. ', color='yellow', s_style='italic')
            print('')
            continue

        cmd, *args = parse_input(user_input)
        
        if cmd == '':
            console.print('Please enter a command.', style='yellow italic')
            continue
        elif cmd in ["close", "exit"]:
            contacts.close()
            break
        elif cmd == 'hello':
            typing_output('Hello, Neo...  ')
            typing_output('I am your assistant bot. ')
            typing_output('I can help you with your contacts and notes. ')
            typing_output('To see the list of available commands, please type "help". ')
        elif cmd == 'help':
            show_help()
        # Contact commands 
        elif cmd == 'add contact': #()
            contacts.add()
        elif cmd == 'find contact': #(name)
            contacts.find(*args)
        elif cmd == 'remove contact': #(name)
            contacts.remove(*args)
        elif cmd == "all contacts":  # ()
            contacts.all()
        elif cmd == "add phone":  # (name, phone number)
            contacts.add_phone(*args)
        elif cmd == "change phone":  # (name, old phone number , new phone number)
            contacts.change_phone(*args)
        elif cmd == "show phone":  # (name)
            contacts.show_phone(*args)
        elif cmd == "delete phone":  # (name, phone number)
            contacts.delete_phone(*args)
        elif cmd == "add email":  # (name, email)
            contacts.add_email(*args)
        elif cmd == "change email":  # (name, old email, new email)
            contacts.change_email(*args)
        elif cmd == "show email":  # (name)
            contacts.show_email(*args)
        elif cmd == "delete email":  # (name, email)
            contacts.delete_email(*args)
        elif cmd == "add birthday":  # (name, birthday)
            contacts.add_birthday(*args)
        elif cmd == "show birthday":  # (name)
            contacts.show_birthday(*args)
        elif cmd == "update birthday":  # (name, new birthday)
            contacts.update_birthday(*args)
        elif cmd == "all birthdays":  # (name, days_to_upcoming)
            contacts.all_birthdays()
        elif cmd == 'export contacts': #()
            contacts.export_contacts_to_csv()
        # Notes commands
        # logic for notes
        else:
            print('')
            console.print('Unknown command ⚠️', style='red bold')
            console.print('To get info about available commands, please type [blue]"help"[/] ', style='yellow italic')
            print('')
         
if __name__ == '__main__':
    main()
