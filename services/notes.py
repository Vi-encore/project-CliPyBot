# do you code here
# Maybe add function edit_note, that will show note book, ask what note you would like to edit (by title), and than will ask which part of note to edit (title, content or tags possibly)

from data.state import notes
from decorators.decorators import input_error, check_arguments
from models.note import Note
from helpers.helpers import save_notes
from helpers.typing_effect import typing_output, typing_input
from rich.console import Console
from helpers.create_table import (show_notes_in_table, show_all_notes_table)

console = Console()

def show_note(note):
    print("")
    show_notes_in_table(note)
    print("")
    return



# def parse_tags(tags_input: str) -> list:
#     if not tags_input:
#         return []
#     return [tag.strip() for tag in tags_input.split(",") if tag.strip()]


# @input_error
# def add():
#     title = input("Enter a title: ")
#     content = input("Enter note content: ")
#     tags_input = input("Enter tag(s) separated by commas: ")
#     tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []

#     tags = parse_tags(tags_input)

#     note = Note(title, content, tags)
#     notes_book.add_note(note)
#     print("Note added successfully!")


def all():
    if not notes.data:
        typing_output(f"No notes found")
        return 1

    print("")
    all_notes = notes.data.values()
    show_all_notes_table(all_notes)
    print("")

    return 0

@input_error
def add():
    title = typing_input("Title: (str): ")
    if not title:
        console.print("Title is required to create a note. ❗", style="red")
        return 1

    note = notes.find_note(title)
    if not note:
        note = Note(title)
        notes.add_note(note)
        typing_output("New contact created.")
    else:
        typing_output("Contact already exists.")
        typing_output("Updating details...")

    # Loop for phone
    while True:
        content = typing_input("Enter a content for a note (press Enter to skip): (str) ").strip()
        if not content:
            break
        try:
            note.add_content(content)
            break
        except Exception as e:
            console.print("Invalid content.❗ ", style="red")
            typing_output("Please try again. ", color="yellow")

    # Loop for email
    while True:
        tag = typing_input("Note tag (press Enter to skip): (str): ").strip()
        if not tag:
            break
        try:
            note.add_tag(tag)
            break
        except Exception as e:
            console.print("Invalid tag ❗ ", style="red")
            typing_output("Please try again. ", color="yellow")

    save_notes(notes)

    typing_output(f'Note "{title}" saved successfully. ✅', color="green")
    # show_contact(record)  # show contact details in table
    show_note(note)
    # print(note)
    return 0


@input_error
def find():
    key_word = input("Enter keyword to search: ")
    results = find(key_word)

    if not results:
        print("No notes found.")
    else:
        for note in results:
            print(note)


@input_error
def change():
    title = input("Enter the title of the note to change: ")
    new_content = input("Enter new content: ")


@input_error
def delete():
    title = input("Enter the title of the note to delete: ")

    if title in notes_book:
        notes_book.delete(title)

    print("Note deleted.")
