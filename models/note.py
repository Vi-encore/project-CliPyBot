from datetime import datetime
from collections import UserDict

# from ..decorators.decorators import input_error
# from decorators.decorators import input_error

# from decorators import decorators
# from .decorators import exception_handler


# print(decorators)


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Title(Field):
    def __init__(self, title: str):
        super().__init__(title)


class Content(Field):
    def __init__(self, content: str):
        super().__init__(content)


# Creating a tag
class Tag(Field):  # add strip
    def __init__(self, tag: str):
        tag = self.create_tag(tag)
        super().__init__(tag)

    def create_tag(self, tag):
        tag = f"#{tag.replace(' ', "_")}"
        return tag


class Note:
    def __init__(self, title=None):
        self.title = Title(title)
        self.content = ''
        self.tags = []

    # === TAGS ===
    def add_tag(self, tag: str):
        if len(self.tags) < 10 and len(tag) <= 25:
            self.tags.append(Tag(tag))
        else:
            raise ValueError("Maximum tags limit exceeded or tag length is invalid.")

    def delete_tag(self, tag: str):
        before = len(self.tags)
        self.tags = [t for t in self.tags if t.value != tag]
        if len(self.tags) == before:
            raise ValueError(f"Tag '{tag}' not found.")

    def edit_tag(self, old_tag: str, new_tag: str):
        for i, tag in enumerate(self.tags):
            if tag.value == old_tag:
                self.tags[i] = Tag(new_tag)
                return
        raise ValueError(f"Tag '{old_tag}' not found.")

    # === CONTENT ===
    def edit_content(self, new_content: str):
        if len(new_content) <= 20000:
            self.content.value = new_content
        else:
            raise ValueError("Content length should not exceed 20000 characters.")

    # === TITLE ===
    def edit_title(self, new_title: str):
        if len(new_title) <= 1000:
            self.title.value = new_title
        else:
            raise ValueError("Title length should not exceed 1000 characters.")

    def __str__(self):
        title = self.title.value if self.title else "None"
        content = self.content.value if self.content else "None"
        tags = "; ".join(tag.value for tag in self.tags) if self.tags else "None"
        return f"Title: {title}, Content: {content}, Tags: {tags}"

    def get_display_data(self):
        """Returns title, content, and tags (as strings)"""
        title = self.title.value if self.title else "None"
        content = self.content.value if self.content else "None"
        tags = [tag.value for tag in self.tags]
        return title, content, tags


class NotesBook(UserDict):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "\n".join(str(note) for note in self.data.values())

    def add_note(self, note: Note):
        self.data[note.title.value] = note

        # if (
        #     note and note.title and note.content
        # ):  # Ensure note has valid title and content
        #     self.data[note.title.value] = note
        #     return f"Note with title '{note.title.value}' has been added."
        # else:
        #     return "Failed to add note. Ensure the note has a title and content."

    # @input_error  # will trigger ModuleNotFound error if run from here ???
    def find_note(self, title):
        return self.data.get(title, None)

    # @input_error  # will trigger ModuleNotFound error if run from here ???
    def delete_note(self, title):
        # check if title still in data
        if title in self.data:
            self.data.pop(title)
            return f"Note {title} has been deleted"
        else:
            return "There is no note with that title"


# Create a NotesBook and add a sample Note
# book = NotesBook()
# # note = Note()
# # created_note = (
# #     note.create_note()
# # )  ated_note)# Ensure create_note() returns the `self` Note instance
# # book.add_note(cre
# # second_note = Note().create_note()
# # book.add_note(second_note)
# book.add_note("Title")
# # book.add_note(Note().create_note())

# print(book)

# # Edit the content of the note
# # title = created_note.title.value
# to_edit = book.find_note("title2")

# print(book)

# # book.delete_note("title1")


# # to_edit.edit_title()
# to_edit.edit_tag()

# print(book)

# # print(edited_note)

# # print(result)
# # print(book.find_note(second_note.title.value))
# # Display all notes in the NotesBook
# # print(book)
# Create a NotesBook instance
notes_book = NotesBook()

# Create a Note instance
note1 = Note(title="Shopping List")

# Add the note to NotesBook
print(notes_book.add_note(note1))  # Output: Note with title 'Shopping List' has been added.

# Find the note by title
retrieved_note = notes_book.find_note("Shopping List")
print(retrieved_note)  # Output: Title: Shopping List, Content: Eggs, Milk, Bread, Tags: None

# Delete the note
print(notes_book.delete_note("Shopping List"))  # Output: Note Shopping List has been deleted.

# Verify the note is deleted
print(notes_book.find_note("Shopping List"))  # Output: None