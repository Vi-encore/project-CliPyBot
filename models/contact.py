import re
import datetime as dt
from datetime import datetime as dtdt
from decorators.decorators import exception_handler

#  Field
class Field():
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)

# Name
class Name(Field):
    def __init__(self, name: str):
        super().__init__(name)
    
# Phone  
class Phone(Field):
    def __init__(self, phone: str):
        self.validate_phone(phone)
        super().__init__(phone)
    def validate_phone(self, phone):
        if not re.match(r'^\d{10}$', phone):
            raise ValueError(f'Invalid phone number: {phone}. Phone must be exactly 10 digits')

class Email(Field):
    def __init__(self, email: str):
        self.validate_email(email)
        super().__init__(email)
        
    def validate_email(self, email):
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, email):
            raise ValueError(f"Invalid email format: {email}")
        
# Birthday
class Birthday(Field): 
    def __init__(self, value: str):
            self.validate_date(value)
            super().__init__(value)
    
    def validate_date(self, value):
        try:
            dtdt.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError('Invalid date format. Use DD.MM.YYYY')
       
# Record
class Record():
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    # === PHONE ===
    @exception_handler
    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))
      
    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    @exception_handler
    def edit_phone(self, phone: str, new_phone: str):
        for p in self.phones:
            if p.value == phone:
                p.value = new_phone
                return
        raise ValueError(f'Phone number {phone} is not found')
    
    # === EMAIL ===
    @exception_handler
    def add_email(self, email):
        self.email = Email(email)
    
    @exception_handler
    def update_email(self, new_email: str):
        """Change the existing email."""
        self.email = Email(new_email)
    
    @exception_handler
    def remove_email(self):
        """Remove the email for the contact."""
        self.email = None
       
    # === BIRTHDAY ===
    @exception_handler
    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)
             
    def __str__(self):
        phone_str = "; ".join(p.value for p in self.phones)
        email_str = f", email: {self.email.value}" if self.email else ""
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phone_str}{email_str}{birthday_str}"

# AddressBook
class AddressBook():
    def __init__(self):
        self.data = {}
    
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    @exception_handler
    def find(self, name: str):
        if name in self.data:
            return self.data[name]
        return None
        
    @exception_handler
    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f'Record {name} is not found')
    
    @exception_handler
    def get_upcoming_birthdays(self) -> list:
        result = []
        today = dt.date.today()
        current_year = today.year
        
        # Calculate the range for next Monday to Friday
        days_to_monday = (7 - today.weekday()) % 7
        next_monday = today + dt.timedelta(days=days_to_monday)
        next_friday = next_monday + dt.timedelta(days=4)
        days_to_next_friday = (next_friday - today).days
        
        for record in self.data.values():
            if not record.birthday:
                continue
            try:
                birthday_str = record.birthday.value
                birthday_obj = dtdt.strptime(birthday_str, "%d.%m.%Y").date()
            except ValueError: 
                raise ValueError(f"Invalid date format for {record.name.value}")
            # get birthday this year
            birthday_this_year = dt.date(current_year, birthday_obj.month,birthday_obj.day)
            if birthday_this_year < today:
                birthday_this_year = dt.date(current_year + 1, birthday_obj.month, birthday_obj.day)
                
            days_to_birthday = (birthday_this_year - today).days
            day_of_birthday = birthday_this_year.weekday()
            
            if days_to_birthday < days_to_next_friday:
                congratulation_date = birthday_this_year
                # If birthday is on Saturday (5) or Sunday (6), move to Monday
                if day_of_birthday in [5, 6]:
                    congratulation_date = next_monday

                result.append({'name': record.name.value, 'congratulation_date': congratulation_date.strftime("%d.%m.%Y")})

        return result
    
    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())