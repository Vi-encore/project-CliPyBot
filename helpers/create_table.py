from rich.console import Console
from rich.table import Table
from rich import box
from datetime import datetime as dtdt

# Initialize Console for rich output
console = Console()


# SHOW CONTACT
def show_contact_in_table(record):
    """ Function to display contact details in a table """
    name, phones, emails, birthday, address = record.get_display_data()
    
    table = Table(
        show_header=True,  # Show header
        header_style="bold green",  # Customize header style
        box=box.ROUNDED,  # Customize table shape
        title=f"{name} 👨",  # Title for the table
        title_justify="center",  # Center the title
        title_style="bold dark_green",  # Title style
    )
    table.add_column("Name", style="dark_green", width=20)
    table.add_column("Phones", justify="left", width=20)
    table.add_column("Emails", justify="left", width=20)
    table.add_column("Birthday", justify="left", width=20)
    table.add_column("Address", justify="left", width=20)

    # Format phones and emails with new lines
    phones_str = "\n".join(phones) if phones else "-"
    emails_str = "\n".join(emails) if emails else "-"
    
    table.add_row(name, phones_str, emails_str, birthday or "-", address or "-")

    # Display the table
    console.print(table)


# SHOW ALL CONTACTS
def show_all_contacts_table(records):
    """Display all contacts in a single styled table"""
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
    table.add_column("Address", justify="left", width=20)

    for record in records:
        name, phones, emails, birthday, address = record.get_display_data()
        phones_str = "\n".join(phones) if phones else "-"
        emails_str = "\n".join(emails) if emails else "-"
        table.add_row(name, phones_str, emails_str, birthday or "-", address or "-")
        table.add_section()  # Adds a separating line between contacts

    console.print(table)


# SHOW BIRTHDAYS
def show_birthdays_table(birthdays):
    """Display birthdays in a styled table"""
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
    table.add_column("Days to birthday", justify="left", width=20)

    today = dtdt.today().date()

    for record in birthdays:
        birthday_date = dtdt.strptime(record["birthday"], "%d.%m.%Y").date()
        delta_days = (birthday_date - today).days

        word_day = "day" if delta_days == 1 else "days"

        # print(f"{record['name']} has birthday on {record['birthday']} in {delta_days} {word_day}.")

        table.add_row(
            record["name"],
            birthday_date.strftime("%d.%m.%Y"),
            f"{delta_days} {word_day}",
        )
        table.add_section()  # Adds a separating line between contacts

    console.print(table)


# SHOW QUERY OPTIONS
def show_options_for_query():
    """Display query options in a styled table"""
    table = Table(
        show_header=True,
        header_style="bold green",
        box=box.ROUNDED,
        title="Query Options 🔍",
        title_justify="center",
        title_style="bold dark_green",
    )
    table.add_column("Option", style="bold white on green", width=20)
    table.add_column("Description", justify="left")

    table.add_row("1", "Search by [bold cyan]name[/]")
    table.add_section()  # Adds a separating line between contacts
    table.add_row("2", "Search by [bold cyan]phone number[/]")
    table.add_section()  # Adds a separating line between contacts
    table.add_row("3", "Search by [bold cyan]email[/] address")
    table.add_section()  # Adds a separating line between contacts
    table.add_row("4", "Search by [bold cyan]birthday[/]")

    console.print(table)


def show_notes_in_table(note):
    # """ Function to display contact details in a table """
    title, content, tags = note.get_display_data()

    table = Table(
        show_header=True,  # Show header
        header_style="bold green",  # Customize header style
        box=box.ROUNDED,  # Customize table shape
        title=f"{title} 👨",  # Title for the table
        title_justify="center",  # Center the title
        title_style="bold dark_green",  # Title style
    )
    table.add_column("Title", style="dark_green", width=20)
    table.add_column("content", justify="left", width=50)
    table.add_column("tags", justify="left", width=20)
    # Format phones and emails with new lines
    tags_str = "\n".join(tags) if tags else "-"
    # emails_str = "\n".join(emails) if emails else "-"

    table.add_row(title, content, tags_str or "-")
    # Display the table
    console.print(table)


def show_all_notes_table(notes):
    """Display all contacts in a single styled table"""
    if not notes:
        console.print("[bold red]No notes to display.[/]")
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
    table.add_column("content", justify="left", width=50)
    table.add_column("tags", justify="left", width=20)
    # print(notes.data)
    # tags_str = "\n".join(tags) if tags else "-"

    for note in notes:
        # print(note.tags)
        # print(note.title, str(note))
        title, content, tags = note.get_display_data()
        # title, content, tags = note #???
        tags = note.tags if note.tags else []
        tags_str = ",".join(tag.value for tag in tags)
        # table.add_row(title, content, tags_str or "-")

        # emails_str = "\n".join(emails) if emails else "-"
        table.add_row(title, content, tags_str or "-")
        table.add_section()  # Adds a separating line between contacts

    console.print(table)

def show_options_for_query_notes():
    """Display query options in a styled table"""
    table = Table(
        show_header=True,
        header_style="bold green",
        box=box.ROUNDED,
        title="Query Options 🔍",
        title_justify="center",
        title_style="bold dark_green",
    )
    table.add_column("Option", style="bold white on green", width=20)
    table.add_column("Description", justify="left")

    table.add_row("1", "Search by [bold cyan]title[/]")
    table.add_section()  # Adds a separating line between contacts
    table.add_row("2", "Search by [bold cyan]content[/]")
    table.add_section()  # Adds a separating line between contacts
    table.add_row("3", "Search by [bold cyan]tag[/]")

    console.print(table)