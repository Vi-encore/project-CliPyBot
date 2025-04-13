import re
import datetime as dt
from datetime import datetime as dtdt, timedelta
from decorators.decorators import exception_handler
from helpers.validators import validate_and_normalize_phone
from helpers.validators import standardize_name


class Field:
    """
    Base class for all fields in the address book.

    Attributes:
        value: The value stored in the field.
    """

    def __init__(self, value) -> None:
        """
        Initialize a Field object.

        Args:
            value: The value to be stored in the field.
        """
        self.value = value

    def __str__(self) -> str:
        """
        Return string representation of the field.

        Returns:
            str: String representation of the field value.
        """
        return str(self.value)


class Name(Field):
    """
    Field for storing contact names with standardization.

    Inherits from Field class.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize a Name object with standardized name.

        Args:
            name (str): The name to be stored.

        Raises:
            ValueError: If the name format is invalid.
        """
        standardized_name = self.normalize_name(name)
        super().__init__(standardized_name)

    def normalize_name(self, name: str) -> str:
        """
        Standardize the name format.

        Args:
            name (str): The name to be standardized.

        Returns:
            str: Standardized name.

        Raises:
            ValueError: If the name format is invalid.
        """
        standardized_name = standardize_name(name)
        if not standardized_name:
            raise ValueError(f"Invalid name format")
        return standardized_name


class Phone(Field):
    """
    Field for storing phone numbers with validation.

    Inherits from Field class.
    """

    def __init__(self, phone: str) -> None:
        """
        Initialize a Phone object with validation.

        Args:
            phone (str): The phone number to be stored.

        Raises:
            ValueError: If the phone number format is invalid.
        """
        valid_phone = self.validate_phone(phone)
        super().__init__(valid_phone)

    def validate_phone(self, phone: str) -> str:
        """
        Validate and normalize phone number.

        Args:
            phone (str): The phone number to validate.

        Returns:
            str: Validated and normalized phone number.

        Raises:
            ValueError: If the phone number format is invalid.
        """
        if not validate_and_normalize_phone(phone):
            raise ValueError(
                f"Invalid phone number: {phone}. Phone must be exactly 10 digits"
            )
        return validate_and_normalize_phone(phone)


class Email(Field):
    """
    Field for storing email addresses with validation.

    Inherits from Field class.
    """

    def __init__(self, email: str) -> None:
        """
        Initialize an Email object with validation.

        Args:
            email (str): The email address to be stored.

        Raises:
            ValueError: If the email format is invalid.
        """
        self.validate_email(email)
        super().__init__(email)

    def validate_email(self, email: str) -> None:
        """
        Validate email format using regex.

        Args:
            email (str): The email to validate.

        Raises:
            ValueError: If the email format is invalid.
        """
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, email):
            raise ValueError(f"Invalid email format: {email}")


class Birthday(Field):
    """
    Field for storing birthday dates with validation.

    Inherits from Field class.
    """

    def __init__(self, value: str) -> None:
        """
        Initialize a Birthday object with validation.

        Args:
            value (str): The birthday date to be stored (DD.MM.YYYY format).

        Raises:
            ValueError: If the date format is invalid.
        """
        self.validate_date(value)
        super().__init__(value)

    def validate_date(self, value: str) -> None:
        """
        Validate date format (DD.MM.YYYY).

        Args:
            value (str): The date to validate.

        Raises:
            ValueError: If the date format is invalid.
        """
        try:
            dtdt.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Address(Field):
    """
    Field for storing contact addresses.

    Inherits from Field class.
    """

    def __init__(self, address: str) -> None:
        """
        Initialize an Address object.

        Args:
            address (str): The address to be stored.
        """
        super().__init__(address)


class Record:
    """
    Class representing a contact record in the address book.

    Contains information about a contact including name, phones, emails,
    birthday, and address.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize a Record object with a name.

        Args:
            name (str): The name of the contact.
        """
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.birthday = None
        self.address = None

    def add_phone(self, phone: str) -> None:
        """
        Add a phone number to the contact.

        Args:
            phone (str): The phone number to add.

        Raises:
            ValueError: If the phone number format is invalid.
        """
        self.phones.append(Phone(phone))

    def find_phone(self, phone: str) -> Phone | None:
        """
        Find a phone number in the contact's phones list.

        Args:
            phone (str): The phone number to find.

        Returns:
            Phone or None: The Phone object if found, None otherwise.
        """
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    @exception_handler
    def change_phone(self, phone: str, new_phone: str) -> None:
        """
        Change a phone number to a new one.

        Args:
            phone (str): The phone number to change.
            new_phone (str): The new phone number.

        Raises:
            ValueError: If the phone number is not found or if the new phone format is invalid.
        """
        for p in self.phones:
            if p.value == phone:
                p.value = Phone(new_phone).value
                return
        raise ValueError(f"Phone number {phone} is not found")

    @exception_handler
    def delete_phone(self, phone: str) -> None:
        """
        Delete a phone number from the contact.

        Args:
            phone (str): The phone number to delete.

        Raises:
            ValueError: If the phone number is not found.
        """
        before = len(self.phones)
        self.phones = [p for p in self.phones if p.value != phone]
        if len(self.phones) == before:
            raise ValueError(f"Phone number {phone} is not found")

    def add_email(self, email: str) -> None:
        """
        Add an email address to the contact.

        Args:
            email (str): The email address to add.

        Raises:
            ValueError: If the email format is invalid.
        """
        self.emails.append(Email(email))

    @exception_handler
    def change_email(self, old_email: str, new_email: str) -> None:
        """
        Change an email address to a new one.

        Args:
            old_email (str): The email address to change.
            new_email (str): The new email address.

        Raises:
            ValueError: If the email is not found or if the new email format is invalid.
        """
        for i, email in enumerate(self.emails):
            if email.value == old_email:
                self.emails[i] = Email(new_email)
                return
        raise ValueError(f"Email '{old_email}' not found.")

    @exception_handler
    def delete_email(self, email: str) -> None:
        """
        Delete an email address from the contact.

        Args:
            email (str): The email address to delete.

        Raises:
            ValueError: If the email is not found.
        """
        before = len(self.emails)
        self.emails = [e for e in self.emails if e.value != email]
        if len(self.emails) == before:
            raise ValueError(f"Email '{email}' not found.")

    def add_birthday(self, birthday: str) -> None:
        """
        Add a birthday to the contact.

        Args:
            birthday (str): The birthday date to add (DD.MM.YYYY format).

        Raises:
            ValueError: If the date format is invalid.
        """
        self.birthday = Birthday(birthday)

    def delete_birthday(self, birthday: str) -> None:
        """
        Delete the birthday from the contact.

        Args:
            birthday (str): The birthday to delete (not used in the function).
        """
        self.birthday = None

    def add_address(self, address: str) -> None:
        """
        Add an address to the contact.

        Args:
            address (str): The address to add.
        """
        self.address = Address(address)

    @exception_handler
    def delete_address(self, name: str) -> None:
        """
        Delete the address from the contact.

        Args:
            name (str): The name parameter (not used in the function).
        """
        self.address = None

    def __str__(self) -> str:
        """
        Return string representation of the contact record.

        Returns:
            str: String representation of the record with all information.
        """
        phone_str = "; ".join(p.value for p in self.phones)
        email_str = "; ".join(e.value for e in self.emails) if self.emails else ""
        birthday_str = f" birthday: {self.birthday.value}" if self.birthday else ""
        address_str = f" address: {self.address.value}" if self.address else ""
        return f"Contact name: {self.name.value}, phones: {phone_str}, emails: {email_str},{birthday_str}, address: {address_str}"

    def get_display_data(self) -> tuple:
        """
        Get display data for the contact record.

        Returns:
            tuple: A tuple containing name, phones list, emails list, birthday, and address.
        """
        name = self.name.value
        phones = [phone.value for phone in self.phones]
        emails = [email.value for email in self.emails]
        birthday = self.birthday.value if self.birthday else None
        address = self.address.value if self.address else None
        return name, phones, emails, birthday, address


class AddressBook:
    """
    Class representing an address book containing contact records.

    Provides methods for adding, finding, and managing contact records.
    """

    def __init__(self) -> None:
        """
        Initialize an AddressBook object.
        """
        self.data = {}

    def add_record(self, record: Record) -> None:
        """
        Add a record to the address book.

        Args:
            record (Record): The record to add.
        """
        self.data[record.name.value] = record

    @exception_handler
    def find(
        self,
        query: str,
        by_name=False,
        by_phone=False,
        by_email=False,
        by_birthday=False,
        by_address=False,
    ) -> list:
        """
        Find records matching a query in the address book.

        Args:
            query (str): The search query.
            by_name (bool, optional): Search by name. Defaults to False.
            by_phone (bool, optional): Search by phone. Defaults to False.
            by_email (bool, optional): Search by email. Defaults to False.
            by_birthday (bool, optional): Search by birthday. Defaults to False.
            by_address (bool, optional): Search by address. Defaults to False.

        Returns:
            list: List of matching records.
        """
        query = query.strip().lower()
        results = []

        for key, record in self.data.items():
            if by_name and query in key.strip().lower():
                results.append(record)
            elif by_phone and any(
                query in phone.value.lower() for phone in record.phones
            ):
                results.append(record)
            elif by_email and any(
                query in email.value.lower() for email in record.emails
            ):
                results.append(record)
            elif (
                by_birthday
                and record.birthday
                and query in record.birthday.value.lower()
            ):
                results.append(record)
            elif (
                by_address and record.address and query in record.address.value.lower()
            ):
                results.append(record)
        return results

    def find_by_name(self, name: str) -> Record | None:
        """
        Find a record by exact name match.

        Args:
            name (str): The name to search for.

        Returns:
            Record or None: The matching record if found, None otherwise.
        """
        if name in self.data:
            return self.data[name]
        return None

    @exception_handler
    def delete(self, name: str) -> None:
        """
        Delete a record from the address book.

        Args:
            name (str): The name of the record to delete.

        Raises:
            ValueError: If the record is not found.
        """
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Record {name} is not found")

    @exception_handler
    def get_birthday_in_days(self, days: int) -> list:
        """
        Get records with birthdays in the specified number of days.

        Args:
            days (int): Number of days to look ahead.

        Returns:
            list: List of dictionaries with names and birthdays.

        Raises:
            ValueError: If a date format is invalid.
        """
        result = []
        today = dt.date.today()
        current_year = today.year
        given_date = today + timedelta(days=days)

        for record in self.data.values():
            if not record.birthday:
                continue
            try:
                birthday_str = record.birthday.value
                birthday_obj = dtdt.strptime(birthday_str, "%d.%m.%Y").date()
            except ValueError:
                raise ValueError(f"Invalid date format for {record.name.value}")
            # get birthday this year
            birthday_this_year = dt.date(
                current_year, birthday_obj.month, birthday_obj.day
            )
            if birthday_this_year < today:
                birthday_this_year = dt.date(
                    current_year + 1, birthday_obj.month, birthday_obj.day
                )

            if today <= birthday_this_year <= given_date:
                result.append(
                    {
                        "name": record.name.value,
                        "birthday": birthday_this_year.strftime("%d.%m.%Y"),
                    }
                )

        return result

    def __str__(self) -> str:
        """
        Return string representation of the address book.

        Returns:
            str: String representation of all records in the address book.
        """
        return "\n".join(str(record) for record in self.data.values())
