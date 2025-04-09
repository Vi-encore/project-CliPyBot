from rich.console import Console
from rich.table import Table
from rich import box

# Initialize Console for rich output
console = Console()

# SHOW CONTACT 
def show_contact_in_table(record):
    """ Function to display contact details in a table """
    name, phones, emails, birthday = record.get_display_data()
    
    table = Table(
        show_header=True,               # Show header
        header_style="bold green",      # Customize header style
        box=box.ROUNDED,                # Customize table shape
        title=f"{name} 👨🏻‍💻",             # Title for the table
        title_justify="center",         # Center the title
        title_style="bold dark_green", # Title style
        )
    table.add_column("Name", style="dark_green", width=20)
    table.add_column("Phones", justify="left", width=20)
    table.add_column("Emails", justify="left", width=20)
    table.add_column("Birthday", justify="left", width=20)

    # Format phones and emails with new lines
    phones_str = "\n".join(phones) if phones else "-"
    emails_str = "\n".join(emails) if emails else "-"
    
    table.add_row(name, phones_str, emails_str, birthday or "-")

    # Display the table
    console.print(table)

# SHOW ALL CONTACTS 
def show_all_contacts_table(records):
    """ Display all contacts in a single styled table """
    if not records:
        console.print("[bold red]No contacts to display.[/]")
        return

    table = Table(
        show_header=True,
        header_style="bold green",
        box=box.ROUNDED,
        title="Contacts List 🗂️",
        title_justify="center",
        title_style="bold dark_green",
    )
    table.add_column("Name", style="bold white on green", width=20)
    table.add_column("Phones", justify="left", width=20)
    table.add_column("Emails", justify="left", width=20)
    table.add_column("Birthday", justify="left", width=20)

    for record in records:
        name, phones, emails, birthday = record.get_display_data()
        phones_str = "\n".join(phones) if phones else "-"
        emails_str = "\n".join(emails) if emails else "-"
        table.add_row(name, phones_str, emails_str, birthday or "-")
        table.add_section()  # Adds a separating line between contacts

    console.print(table)
    
# SHOW BIRTHDAYS 
def show_birthdays_table(birthdays):
    """ Display birthdays in a styled table """
    if not birthdays:
        console.print("[bold red]No birthdays to display.[/]")
        return

    table = Table(
        show_header=True,
        header_style="bold green",
        box=box.ROUNDED,
        title="Birthdays List 🍰",
        title_justify="center",
        title_style="bold dark_green",
    )
    table.add_column("Upcoming Birthdays", style="bold white on green", width=20)
    table.add_column("Birthday", justify="left", width=20)

    for record in birthdays:
        
        table.add_row(record['name'], record['congratulation_date'] or "-")
        table.add_section()  # Adds a separating line between contacts

    console.print(table)