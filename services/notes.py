from data.state import notes
from decorators.decorators import input_error, check_arguments
from models.note import Note
from helpers.helpers import save_notes
from helpers.typing_effect import typing_output, typing_input
from rich.console import Console
from helpers.create_table import (
    show_notes_in_table,
    show_all_notes_table,
    show_options_for_query_notes,
)
from pathlib import Path
import datetime as dt
from datetime import datetime as dtdt
import csv

console = Console()


# Note what type
def show_note(note) -> None:
    print("")
    show_notes_in_table(note)
    print("")
    return


def parse_tags(tags_input: str) -> list:
    if not tags_input:
        return []
    return [
        tag.strip()
        for tag in tags_input.split(",")
        if tag.strip() and len(tag.strip()) <= 25
    ]


def all() -> int:
    # print(notes.data)
    if not notes.data:
        console.print(f"No notes found❗️ ", style="red")
        return 1

    print("")
    all_notes = notes.data.values()
    show_all_notes_table(all_notes)
    print("")

    return 0


@input_error
def add() -> int:
    title = typing_input("Title: (str): ").strip()
    if not title:
        console.print("Title is required to create a note. ❗️", style="red")
        return 1

    note = notes.find_note(title)
    if not note:
        note = Note(title)
        notes.add_note(note)
        typing_output("New note created.")
    else:
        typing_output("Note already exists.", color="yellow")
        typing_output("Updating details...")

    # Loop for content
    while True:
        content = typing_input(
            "Enter a content for a note (press Enter to skip): (str) "
        ).strip()
        if not content:
            break
        try:
            note.add_content(content)
            break
        except Exception as e:
            console.print("Invalid content.❗️ ", style="red")
            typing_output("Please try again. ", color="yellow")

    # Loop for tags
    while True:
        tags = typing_input("Note tag (press Enter to skip): (str): ").strip()
        if not tags:
            break
        try:
            tags_to_add = parse_tags(tags)  # if tag is in tags - do not add
            [note.add_tag(tag) for tag in tags_to_add]
            # [note.add_tag(tag) for tag in tags_to_add if tag not in [t.value for t in note.tags]]
            break
        except Exception as e:
            console.print("Invalid tag ❗️ ", style="red")
            typing_output("Please try again. ", color="yellow")

    save_notes(notes)

    typing_output(f'Note "{title}" saved successfully. ✅', color="green")
    # show_contact(record)  # show contact details in table
    show_note(note)
    # print(note)
    return 0


@input_error
def change_note() -> bool:
    """Edit existing note (content or tags)"""
    try:
        # Check if the notes dictionary is empty
        if not notes.data:
            print("No notes found!")
            return False

        # Display all notes with numbers for reference
        typing_output("\nAvailable notes:")
        titles = list(notes.data.keys())
        for i, title in enumerate(titles, 1):  # Enumerate note titles
            typing_output(f"{i}. {title}")

        # Prompt user to select a note by number
        while True:
            user_choice = input(
                "Enter the number of the note you want to edit (int): "
            ).strip()
            if not user_choice.isdigit():  # Check if input is a valid number
                typing_output(
                    "Invalid input! Please enter a valid number.", color="yellow"
                )
                continue

            note_index = int(user_choice) - 1  # Convert to zero-based index
            if 0 <= note_index < len(titles):
                title = titles[note_index]  # Get the selected note title
                break
            else:
                typing_output(
                    "Invalid number! Please choose a number from the list.",
                    color="yellow",
                )
                return False

        # Find the selected note
        note = notes.find_note(title)
        if not note:
            console.print(f"Note '{title}' not found! ", style="red")
            return False

        # Show current note details
        show_note(note)

        # Prompt user to choose what to edit
        edit_choice = typing_input(
            "\nWhat do you want to edit? (content/tags): "
        ).lower()
        if edit_choice == "content":
            # Handle content editing
            typing_output(f"Current content: {note.content}")
            new_content = typing_input("Enter new content: ")
            if not new_content:
                console.print("Content update skipped!", style="red")
                return False
            try:
                note.edit_content(new_content)
                save_notes(notes)
                show_note(note)
                typing_output("Content updated successfully ✓", color="green")
            except ValueError as e:
                console.print(f"Error updating content: {e}", style="red")
                return False

        elif edit_choice == "tags":
            # Handle tag editing
            tag_action = typing_input(
                "Do you want to (add/edit/delete) tags?: "
            ).lower()

            if tag_action == "add":
                new_tag = typing_input("Enter new tag: ")
                try:
                    if new_tag in [t.value for t in note.tags]:
                        console.print(
                            f"Tag '{new_tag}' already exists!", style="yellow"
                        )
                    else:
                        note.add_tag(new_tag)
                        save_notes(notes)
                        show_note(note)
                        typing_output(
                            f"Tag '{new_tag}' added successfully ✓", color="green"
                        )
                except ValueError as e:
                    console.print(f"Error adding tag: {e}", style="red")
                    return False

            elif tag_action == "edit":
                # Enumerate tags and allow user to select which one to edit
                typing_output(
                    f"Current tags: {', '.join(tag.value for tag in note.tags) if note.tags else 'None'}"
                )
                tags = list(note.tags)  # Convert tags to a list for enumeration
                for i, tag in enumerate(tags, 1):
                    typing_output(f"{i}. {tag.value}")

                while True:
                    tag_choice = input(
                        "Enter the number of the tag you want to edit (int): "
                    ).strip()
                    if not tag_choice.isdigit():
                        typing_output(
                            "Invalid input! Please enter a valid number.",
                            color="yellow",
                        )
                        continue

                    tag_index = int(tag_choice) - 1  # Convert to zero-based index
                    if 0 <= tag_index < len(tags):
                        old_tag = tags[tag_index].value
                        break
                    else:
                        typing_output(
                            "Invalid number! Please choose a number from the list.",
                            color="yellow",
                        )
                        return False

                new_tag = typing_input("Enter new tag value: ")
                try:
                    note.edit_tag(old_tag, new_tag)
                    save_notes(notes)
                    show_note(note)
                    typing_output(
                        f"Tag '{old_tag}' updated to '{new_tag}' successfully ✓",
                        color="green",
                    )
                except ValueError as e:
                    console.print(f"Error editing tag: {e}", style="red")
                    return False

            elif tag_action == "delete":
                # Enumerate tags and allow user to select which one to delete
                typing_output(
                    f"Current tags: {', '.join(tag.value for tag in note.tags) if note.tags else 'None'}"
                )
                tags = list(note.tags)  # Convert tags to a list for enumeration
                for i, tag in enumerate(tags, 1):
                    typing_output(f"{i}. {tag.value}")

                while True:
                    tag_choice = input(
                        "Enter the number of the tag you want to delete (int): "
                    ).strip()
                    if not tag_choice.isdigit():
                        typing_output(
                            "Invalid input! Please enter a valid number.",
                            color="yellow",
                        )
                        continue

                    tag_index = int(tag_choice) - 1  # Convert to zero-based index
                    if 0 <= tag_index < len(tags):
                        tag_to_delete = tags[tag_index].value
                        break
                    else:
                        typing_output(
                            "Invalid number! Please choose a number from the list.",
                            color="yellow",
                        )
                        return False

                try:
                    note.delete_tag(tag_to_delete)
                    save_notes(notes)
                    show_note(note)
                    typing_output(
                        f"Tag '{tag_to_delete}' deleted successfully ✓", color="green"
                    )
                except ValueError as e:
                    console.print(f"Error deleting tag: {e}", style="red")
                    return False
            else:
                print("Invalid tag action!")
                return False

        else:
            print("Invalid choice! Please enter 'content' or 'tags'.")
            return False

        # Confirm the update
        typing_output(f"Note '{title}' updated successfully ✓", color="green")
        return True

    except Exception as e:
        console.print(f"Error editing note: {e}", style="red")
        return False


@input_error
def delete_note() -> bool:
    """Delete note, content, or tags"""
    try:
        # Check if the notes dictionary is empty
        if not notes.data:
            console.print("No notes found!", style="red")
            return False

        # Display all notes with numbers for reference
        typing_output("\nAvailable notes:")
        titles = list(notes.data.keys())
        for i, title in enumerate(titles, 1):
            typing_output(f"{i}. {title}")

        # Prompt user to select a note by number
        while True:
            user_choice = input(
                "Enter the number of the note you want to delete (int): "
            ).strip()
            if not user_choice.isdigit():  # Check if input is numeric
                typing_output(
                    "Invalid input! Please enter a valid number.", color="yellow"
                )
                continue

            note_index = int(user_choice) - 1  # Convert to zero-based index
            if 0 <= note_index < len(titles):
                title = titles[note_index]  # Retrieve the selected note title
                break
            else:
                typing_output(
                    "Invalid number! Please choose a number from the list.",
                    color="yellow",
                )
                return False

        # Find the selected note
        note = notes.find_note(title)
        if not note:
            console.print(f"Note '{title}' not found!", style="red")
            return False

        # Prompt user to choose what to delete
        delete_choice = typing_input(
            "What do you want to delete? (all/content/tags): "
        ).lower()
        if delete_choice == "all":
            # Delete the entire note
            notes.delete_note(title)
            show_all_notes_table(notes)  # Example: Display updated notes
            typing_output(f"Note '{title}' deleted successfully ✓", color="green")

        elif delete_choice == "content":
            # Delete the content only
            note.delete_content()
            save_notes(notes)
            show_note(note)
            typing_output(
                f"Content of note '{title}' deleted successfully ✓", color="green"
            )

        elif delete_choice == "tags":
            # Handle tag deletion (all or specific tags)
            tag_delete_mode = typing_input(
                "Delete (all) tags or a (specific) tag? "
            ).lower()
            if tag_delete_mode == "all":
                note.tags = []  # Clear all tags
                save_notes(notes)
                show_note(note)
                typing_output(
                    f"All tags of note '{title}' deleted successfully ✓", color="green"
                )

            elif tag_delete_mode == "specific":
                typing_output(
                    f"Current tags: {', '.join(tag.value for tag in note.tags) if note.tags else 'None'}"
                )
                tag_to_delete = typing_input("Enter tag to delete: ").strip()
                try:
                    note.delete_tag(tag_to_delete)
                    save_notes(notes)
                    show_note(note)
                    typing_output(
                        f"Tag '{tag_to_delete}' deleted successfully ✓", color="green"
                    )
                except ValueError as e:
                    console.print(f"Error deleting tag: {e}", style="red")
                    return False
            else:
                console.print("Invalid tag deletion mode.", style="red")
                return False

        else:
            console.print("You did not choose a valid option!", style="red")
            return False

        return True

    except Exception as e:
        console.print(f"Error deleting note components: {e}", style="red")
        return False


@input_error
def export_notes_to_csv() -> None:
    today = dtdt.now().strftime("%d.%m.%Y")
    filename = f"notes_{today}.csv"

    STORAGE_DIR = Path(__file__).parent.parent / "storage"
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    default_path = STORAGE_DIR / filename

    dir_path = typing_input(
        f"Enter the path to save the CSV file (press Enter for default save) 🗄️: "
    ).strip()
    if dir_path:
        filepath = Path(dir_path) / filename
    else:
        filepath = default_path

    # Check if the directory exists
    if not filepath.parent.exists():
        console.print(
            f"Error: The directory '{filepath.parent}' does not exist. 🚨", style="red"
        )

        create_dir = (
            typing_input(
                f"Would you like to create the directory '{filepath.parent}'? (y/n): 💊"
            )
            .strip()
            .lower()
        )
        if create_dir == "y":
            filepath.parent.mkdir(parents=True, exist_ok=True)
            typing_output(f"Directory '{filepath.parent}' created. ✅", color="green")
        else:
            console.print("Aborting export. ⛔", style="red")
            return

    # Check if the file is writable (optional, we just try opening it for writing)
    try:
        with filepath.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Title", "Content", "Tags"])
            for note in notes.data.values():
                writer.writerow(
                    [
                        note.title,
                        note.content if note.content else "",
                        ", ".join(t.value for t in note.tags),
                    ]
                )
        typing_output(f"Contacts saved to: {filepath} 💾")

    except (OSError, IOError) as e:
        console.print(f"Error writing to file: {e} 🚨 ", style="red")


# what to do here code in Bolma
@input_error
def find():
    print("")
    show_options_for_query_notes()
    print("")

    # Loop for query
    while True:
        query = (
            typing_input(
                "How do you want to search (Enter the number of field): (num) "
            )
            .strip()
            .lower()
        )

        if not query:
            typing_output("No input provided❗", color="yellow")
            typing_output("You can enter any other command")
            return 1

        if query not in ["1", "2", "3"]:
            typing_output(
                "Invalid option. Please enter a number between 1 and 3. ❗",
                color="yellow",
            )
            continue
        break

    # Get args based on query
    if query == "1":  # search by name
        args = typing_input("Enter a title of the note: (str): ").strip().split()
    elif query == "2":
        args = typing_input("Enter a content: (str): ").strip().split()
    elif query == "3":
        args = typing_input("Enter a tag: (str): ").strip().split()
    else:
        typing_output(
            "Invalid option. Please enter a number between 1 and 3. ❗", color="yellow"
        )
        return 1
    if not args:
        typing_output(
            "No input provided. Please enter a valid query. ❗", color="yellow"
        )
        return 1

    # Call the find method with the appropriate arguments
    if query == "1":  # search by name
        result = notes.search(" ".join(args), by_title=True)
    elif query == "2":  # search by phone
        result = notes.search(" ".join(args), by_content=True)
    elif query == "3":  # search by email
        result = notes.search(" ".join(args), by_tag=True)
    else:
        typing_output(
            "Invalid option. Please enter a number between 1 and 3. ❗", color="yellow"
        )
        return 1

    if not result:
        typing_output("No note found. ❗", color="yellow")
        return 1
    # If a record is found, show the contact details

    print("")
    typing_output("Note found:")
    show_all_notes_table(result)  # show contacts details in table
    print("")
    return 0


@input_error
def display_note():
    if not notes.data:
        typing_output("The contact book is empty ", color="yellow")
        return

    for index, title in enumerate(notes.data.keys(), 1):
        typing_output(f"{index}. {title}")
    while True:
        what_contact = input("Enter number of contact you want to show (int): ")
        if not what_contact:
            typing_output(f"You did not chose any note", color="yellow")  # ??
            try_again = input("Would you like to try again? (y/n): ").lower()
            if try_again != "y":
                print("Exiting note selection.")
                return
        elif not what_contact.isdigit():  # Check if the input is not a number
            typing_output("Invalid input! Please enter a valid number.", color="yellow")
        else:
            selected_index = int(what_contact) - 1
            if 0 <= selected_index < len(notes.data):
                # selected_name = book.find_by_name(name)
                selected_name = list(notes.data.keys())[selected_index]
                show_note(notes.find_note(selected_name))
                break
            else:
                typing_output(
                    "Invalid note number. Please select from the list", color="yellow"
                )
                return
