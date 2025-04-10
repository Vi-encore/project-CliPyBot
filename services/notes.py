# do you code here
# Maybe add function edit_note, that will show note book, ask what note you would like to edit (by title), and than will ask which part of note to edit (title, content or tags possibly)
from models.note import Note, NotesBook
from decorators.decorators import input_error, check_arguments


notes_book = NotesBook()

def parse_tags(tags_input: str) -> list:
    if not tags_input:
        return []
    return [tag.strip() for tag in tags_input.split(",") if tag.strip()]


@input_error
def add():
    title = input("Enter a title: ")
    content = input("Enter note content: ")
    tags_input = input("Enter tag(s) separated by commas: ")
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []

    tags = parse_tags(tags_input)

    note = Note(title, content, tags)
    notes_book.add_note(note)
    print("Note added successfully!")


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

