from rich.console import Console
from rich.table import Table
from rich import box
from datetime import datetime as dtdt

# Initialize Console for rich output
console = Console()


# SHOW CONTACT
def show_contact_in_table(record) -> None:
    """
    Display details of a single contact in a formatted table.

    Args:
        record: The contact record containing details such as name, phones, emails,
                birthday, and address.

    Returns:
        None
    """
    name, phones, emails, birthday, address = record.get_display_data()

    table = Table(
        show_header=True,  # Show header
        header_style="bold green",  # Customize header style
        box=box.ROUNDED,  # Customize table shape
        title=f"{name} 👨",  # Title for the table
        title_justify="center",  # Center the title
        title_style="bold sea_green3",  # Title style
    )
    table.add_column("Name", style="sea_green3", width=20)
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
def show_all_contacts_table(records) -> None:
    """
    Display all contacts in a single styled table.

    Args:
        records: A list of contact records, where each record contains details
                such as name, phones, emails, birthday, and address.

    Returns:
        None
    """
    if not records:
        console.print("[bold red]No contacts to display.[/]")
        return

    table = Table(
        show_header=True,
        header_style="bold green",
        box=box.ROUNDED,
        title="Contacts List 🗂️",
        title_justify="center",
        title_style="bold sea_green3",
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
def show_birthdays_table(birthdays) -> None:
    """
    Display upcoming birthdays in a styled table.

    Args:
        birthdays: A list of dictionaries, where each dictionary represents
                a contact with their name and birthday details.

    Returns:
        None
    """
    if not birthdays:
        console.print("[bold red]No birthdays to display.[/]")
        return

    table = Table(
        show_header=True,
        header_style="bold green",
        box=box.ROUNDED,
        title="Birthdays List 🍰",
        title_justify="center",
        title_style="bold sea_green3",
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
def show_options_for_query() -> None:
    """
    Display search query options for contacts in a styled table.

    The options include searching by name, phone number, email, birthday, or address.

    Returns:
        None
    """
    table = Table(
        show_header=True,
        header_style="bold green",
        box=box.ROUNDED,
        title="Query Options 🔍",
        title_justify="center",
        title_style="bold sea_green3",
    )
    table.add_column("Option", style="bold white on green", width=20)
    table.add_column("Description", justify="left")

    table.add_row("1", "Search by [bold cyan]name[/]")
    table.add_section()  # Adds a separating line between contacts
    table.add_row("2", "Search by [bold cyan]phone number[/]")
    table.add_section()
    table.add_row("3", "Search by [bold cyan]email[/] address")
    table.add_section()
    table.add_row("4", "Search by [bold cyan]birthday[/]")
    table.add_section()
    table.add_row("5", "Search by [bold cyan]address[/]")

    console.print(table)


# SHOW NOTES
def show_notes_in_table(note) -> None:
    """
    Display details of a single note in a formatted table.

    Args:
        note: The note record containing details such as title, content, and tags.

    Returns:
        None
    """
    title, content, tags = note.get_display_data()

    table = Table(
        show_header=True,  # Show header
        header_style="bold green",  # Customize header style
        box=box.ROUNDED,  # Customize table shape
        title=f"{title} 👨",  # Title for the table
        title_justify="center",  # Center the title
        title_style="bold sea_green3",  # Title style
    )
    table.add_column("Title", style="sea_green3", width=20)
    table.add_column("Content", justify="left", width=50)
    table.add_column("Tags", justify="left", width=20)
    # Format phones and emails with new lines
    tags_str = "\n".join(tags) if tags else "-"

    table.add_row(title, content, tags_str or "-")
    console.print(table)


# SHOW ALL NOTES
def show_all_notes_table(notes) -> None:
    """
    Display all notes in a single styled table.

    Args:
        notes: A list of note records, where each record contains details
            such as title, content, and tags.

    Returns:
        None
    """
    if not notes:
        console.print("[bold red]No notes to display.[/]")
        return

    table = Table(
        show_header=True,
        header_style="bold green",
        box=box.ROUNDED,
        title="Notes List 🗂️",
        title_justify="center",
        title_style="bold sea_green3",
    )
    table.add_column("Title", style="bold white on green", width=20)
    table.add_column("Content", justify="left", width=50)
    table.add_column("Tags", justify="left", width=20)

    for note in notes:
        title, content, tags = note.get_display_data()
        content = content if note.content else "-"
        tags = note.tags if note.tags else []
        tags_str = ",".join(tag.value for tag in tags) if note.tags else "-"
        table.add_row(title, content, tags_str)
        table.add_section()  # Adds a separating line between notes

    console.print(table)


# SHOW QUERY OPTIONS FOR NOTES
def show_options_for_query_notes() -> None:
    """
    Display search query options for notes in a styled table.

    The options include searching by title, content, or tags.

    Returns:
        None
    """
    table = Table(
        show_header=True,
        header_style="bold green",
        box=box.ROUNDED,
        title="Query Options 🔍",
        title_justify="center",
        title_style="bold sea_green3",
    )
    table.add_column("Option", style="bold white on green", width=20)
    table.add_column("Description", justify="left")

    table.add_row("1", "Search by [bold cyan]title[/]")
    table.add_section()
    table.add_row("2", "Search by [bold cyan]content[/]")
    table.add_section()
    table.add_row("3", "Search by [bold cyan]tag[/]")

    console.print(table)
