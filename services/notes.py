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
    # all()
    """Edit existing note (content or tags)"""
    try:
        # Display all notes for reference
        if not notes.data:
            print("No notes found!")
            return False

        typing_output("\nAvailable notes:")
        for i, title in enumerate(notes.data.keys(), 1):
            typing_output(f"{i}. {title}")

        # Get note to edit
        title = typing_input("\nEnter the title of the note to edit: ").strip()
        note = notes.find_note(title)

        if not note:
            console.print(f"Note '{title}' not found! ", style="red")
            return False

        # Show current note details
        show_note(note)

        # Choose what to edit
        edit_choice = typing_input(
            "\nWhat do you want to edit? (content/tags): "  # if noting here - you did not chose any option
        ).lower()

        if edit_choice == "content":
            # Edit content
            typing_output(f"Current content: {note.content}")  # typing
            new_content = typing_input("Enter new content: ")
            if not new_content:
                console.print("Content update skipped! ", style="red")
                return False
                # new_content = "-"

            try:
                note.edit_content(new_content)
                save_notes(notes)
                show_note(note)
                typing_output(
                    "Content updated successfully ✓ ", color="green"
                )  # typing
            except ValueError as e:
                console.print(f"Error updating content: {e} ", style="red")
                # print(f"Error updating content: {e}")
                return False

        elif edit_choice == "tags":
            # Edit tags
            tag_action = typing_input(
                "Do you want to (add/edit/delete) tags?: "
            ).lower()

            if tag_action == "add":
                # Add new tag
                new_tag = typing_input("Enter new tag: ")
                try:
                    if new_tag in [t.value for t in note.tags]:  # will that break?
                        console.print(f"Tag {new_tag} already exists! ", style="yellow")
                    else:
                        note.add_tag(new_tag)

                    save_notes(notes)
                    show_note(note)
                    typing_output(
                        f"Tag '{new_tag}' added successfully ✓ ", color="green"
                    )  # typing

                except ValueError as e:
                    console.print(f"Error adding tag: {e} ", style="red")
                    return False

            elif tag_action == "edit":
                # Edit existing tag
                typing_output(
                    f"Current tags: {', '.join(tag.value for tag in note.tags) if note.tags else 'None'}"
                )
                old_tag = typing_input("Enter tag to edit: ")
                new_tag = typing_input("Enter new tag value: ")

                try:
                    note.edit_tag(old_tag, new_tag)
                    save_notes(notes)
                    show_note(note)
                    typing_output(
                        f"Tag '{old_tag}' updated to '{new_tag}' successfully ✓  ",
                        color="green",
                    )
                except ValueError as e:
                    console.print(f"Error editing tag: {e} ", style="red")
                    return False

            elif tag_action == "delete":
                # Delete a tag
                typing_output(
                    f"Current tags: {', '.join(tag.value for tag in note.tags) if note.tags else 'None'}"
                )
                tag_to_delete = typing_input("Enter tag to delete: ")

                try:
                    note.delete_tag(tag_to_delete)
                    save_notes(notes)
                    show_note(note)
                    typing_output(
                        f"Tag '{tag_to_delete}' deleted successfully ✓ ", color="green"
                    )
                except ValueError as e:
                    console.print(f"Error deleting tag: {e} ", style="red")
                    return False

            else:
                print("Invalid tag action!")
                return False

        else:
            print("Invalid choice! Please enter 'content' or 'tags'.")
            return False

        # Save notes after edit
        typing_output(f"Note '{title}' updated successfully ✓ ", color="green")
        return True

    except Exception as e:
        console.print(f"Error editing note: {e} ", style="red")
        return False


@input_error
def delete_note() -> bool:
    all()
    """Delete note, content, or tags"""
    try:
        # Display all notes for reference
        if not notes.data:
            console.print(f"No notes found! ", style="red")
            return False

        print("\nAvailable notes:")
        for i, title in enumerate(notes.data.keys(), 1):
            typing_output(f"{i}. {title}")

        # Get note to modify
        title = typing_input("\nEnter the title of the note: ").strip()
        note = notes.find_note(title)
        print(note)

        if not note:
            console.print(f"Note {title} not found! ", style="red")
            return False

        # Choose what to delete
        delete_choice = typing_input(
            "What do you want to delete? (all/content/tags): "
        ).lower()

        if delete_choice == "all":
            # Delete entire note
            notes.delete_note(title)
            show_all_notes_table(notes)
            # show_note(note)
            print(f"Note '{title}' deleted successfully ✓")

        elif delete_choice == "content":
            # Delete just the content
            note.delete_content()
            save_notes(notes)
            show_note(note)
            typing_output(
                f"Content of note '{title}' deleted successfully ✓ ", color="green"
            )

        elif delete_choice == "tags":
            # Delete tags - either all or specific ones
            tag_delete_mode = typing_input(
                "Delete (all) tags or a (specific) tag? "
            ).lower()

            if tag_delete_mode == "all":
                note.tags = []
                save_notes(notes)
                show_note(note)
                typing_output(
                    f"All tags of note '{title}' deleted successfully ✓ ", color="green"
                )

            elif tag_delete_mode == "specific":
                typing_output(
                    f"Current tags: {', '.join(tag.value for tag in note.tags) if note.tags else 'None'}"
                )
                tag_to_delete = typing_input("Enter tag to delete: ")

                try:
                    note.delete_tag(tag_to_delete)
                    save_notes(notes)
                    show_note(note)
                    typing_output(
                        f"Tag '{tag_to_delete}' deleted successfully ✓ ", color="green"
                    )
                except ValueError as e:
                    console.print(f"Error deleting tag: {e} ", style="red")
                    return False

            else:
                console.print(f"Invalid tag deletion mode ", style="red")
                return False

        else:
            console.print(
                f"You did not enter anything!",
                style="red",
            )
            return False

        return True

    except Exception as e:
        console.print(f"Error deleting note components: {e} ", style="red")
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
