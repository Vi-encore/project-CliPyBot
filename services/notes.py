# # do you code here
# # Maybe add function edit_note, that will show note book, ask what note you would like to edit (by title), and than will ask which part of note to edit (title, content or tags possibly)

from data.state import notes
from decorators.decorators import input_error, check_arguments
from models.note import Note
from helpers.helpers import save_notes
from helpers.typing_effect import typing_output, typing_input
from rich.console import Console
from helpers.create_table import show_notes_in_table, show_all_notes_table

console = Console()

def show_note(note):
    print("")
    show_notes_in_table(note)
    print("")
    return


def parse_tags(tags_input: str) -> list:
    if not tags_input:
        return []
    return [tag.strip() for tag in tags_input.split(",") if tag.strip()]





@input_error
def add():
    title = input("Enter a title: ")
    content = input("Enter note content: ")
    tags_input = input("Enter tag(s) separated by commas: ")
    tags = parse_tags(tags_input)

    note = Note(title)
    note.add_content(content)
   
    for tag in tags:
        note.add_tag(tag)

    notes.add_note(note)

    print("Note added successfully!")


@input_error
def find():
    key_word = input("Enter title to search: ")
    results = notes.find_note(key_word)

    if not results:
        print("No notes found.")
    else:
        title, content, tags = results.get_display_data()
        print(f"Title: {title}")
        print(f"Content: {content}")
        print("Tags: " + (", ".join(tags) if tags else "None"))



@input_error
def change():
    title = input("Enter the title of the note to change: ")
    note_for_changing = notes.find_note(title)
    if not note_for_changing:
        print("Note not found.")
        return

    new_content = input("Enter new content: ")
    note_for_changing.edit_content(new_content)
    print("Note content updated.")


@input_error
def delete():
    title = input("Enter the title of the note to delete: ")
    notes.delete_note(title)
    print("Note deleted.")

