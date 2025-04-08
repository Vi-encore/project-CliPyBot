from datetime import datetime
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Do we need some form of validation for note title?
class Title(Field):
    def __init__(self, title: str):
        super().__init__(title)


# Do we need some form of validation for notes?
class Content(Field):
    def __init__(self, content: str):
        super().__init__(content)


# Creating a tag
class Tag(Field):
    def __init__(self, tag: str):
        tag = self.create_tag(tag)
        super().__init__(tag)

    # def __str__

    def create_tag(self, tag):
        tag = f"#{tag}"
        return tag


# print(Tag('tag'))


class Note:
    def __init__(self):
        self.title = None
        self.content = None
        self.tags = []

    def __str__(self) -> str:
        return f"Title: {self.title.value}, content: {self.content.value}, tags: {', '.join(tag.value for tag in self.tags)}."

    def create_note(self):
        new_title = input("Enter a note title: ")
        new_content = input("Enter note content: ")
        create_tag = input("Want to add a tag? (y/n): ").lower()

        new_tags = []
        if create_tag == "y":
            tags = input("Enter your tag(s), separated by commas: ").split(",")
            new_tags = [Tag(tag.strip()) for tag in tags]

        self.title = Title(new_title)
        self.content = Content(new_content)
        self.tags = new_tags

        # Optionally return the formatted string representation
        return self

    # def edit_note(self, title):
    #     # Search for the note by title in the data dictionary
    #     note = self.data.get(title)

    #     if not note:
    #         return f"Note with title '{title}' does not exist."

    #     # Display the current content of the note
    #     print(f"Current Content: {note.content.value}")

    #     # Ask the user for the new content
    #     new_content = input(
    #         "Enter new content (leave empty to keep the current content): "
    #     )

    #     # Update content if the user provides new content
    #     if new_content.strip():
    #         note.content = Content(new_content.strip())
    #         self.data[title] = note  # Save the updated note back to the NotesBook
    #         return f"Content of note with title '{title}' has been updated."
    #     else:
    #         return "No changes were made to the content."
    def edit_content(self):
      is_change = input(f'You want to change that content {self.content.value} for {self.title.value} note? (y/n)')
      old_content = self.content.value
      if is_change == 'y':
        new_content = input('Enter a new content for this note: ')
        self.content.value = new_content
      return f'The content for {self.title.value} has been changed'
    
    


class NotesBook(UserDict):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "\n".join(str(note) for note in self.data.values())

    def add_note(self, note: Note):
        if note.title and note.content:  # Ensure note has valid title and content
            self.data[note.title.value] = note
            return f"Note with title '{note.title.value}' has been added."
        else:
            return "Failed to add note. Ensure the note has a title and content."

    def find_note(self, title): 
      return self.data.get(title, None)

    def delete_note(self, title):
      #check if title still in data
      if title in self.data:
        self.data.pop(title)
        return f'Note {title} has been deleted'
      else:
        return 'There is no note with that title'


# Create a NotesBook and add a sample Note
book = NotesBook()
note = Note()
created_note = (
    note.create_note()
)  # Ensure create_note() returns the `self` Note instance
book.add_note(created_note)
second_note = (Note().create_note())
book.add_note(second_note)
book.add_note(Note().create_note())

# Edit the content of the note
title = created_note.title.value
to_edit= book.find_note(title)



book.delete_note('title1')


print(book)

edited_note = to_edit.edit_content()



# print(edited_note)

# print(result)
# print(book.find_note(second_note.title.value))
# Display all notes in the NotesBook
print(book)
