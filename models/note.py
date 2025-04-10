from datetime import datetime
from collections import UserDict

# from ..decorators.decorators import input_error
from decorators.decorators import input_error

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
        tag = self.create_tag(tag.strip())
        super().__init__(tag)

    def create_tag(self, tag: str) -> str:
        tag = f"#{tag.replace(' ', "_")}"
        return tag


class Note:
    def __init__(self, title: str) -> None:
        self.title = Title(title)
        self.content = None
        self.tags = []

    # === TAGS ===
    @input_error 
    def add_tag(self, tag: str) -> None:
        if len(self.tags) < 10 and len(tag) <= 25:
            self.tags.append(Tag(tag))
        else:
            raise ValueError("Maximum tags limit exceeded or tag length is invalid.")

    def delete_tag(self, tag: str) -> bool:
        for t in self.tags:
            if t.value == tag:
                self.tags.remove(t)
                return True
        raise ValueError(f"Tag '{tag}' not found.")

    @input_error 
    def edit_tag(self, old_tag: str, new_tag: str) -> None:
        for i, tag in enumerate(self.tags):
            if tag.value == old_tag:
                self.tags[i] = Tag(new_tag)
                return
        raise ValueError(f"Tag '{old_tag}' not found.")

    # What it returns (maybe t.value)
    @input_error 
    def find_tag(self, tag: str) -> str | None:
        for t in self.tags:
            if t.value == tag:
                return t
        return None

    # === CONTENT ===
    @input_error 
    def edit_content(self, new_content: str) -> None:
        if len(new_content) <= 20000:
            self.content = new_content
        else:
            raise ValueError("Content length should not exceed 20000 characters.")

    @input_error 
    def add_content(self, content: str) -> None:
        self.content = Content(content).value

    def delete_content(self) -> None:
        self.content = ""

    # === TITLE ===
    @input_error 
    def edit_title(self, new_title: str) -> None:
        if len(new_title) <= 1000:
            self.title = new_title
        else:
            raise ValueError("Title length should not exceed 1000 characters.")

    def __str__(self) -> str:
        title = self.title if self.title else "None"
        content = self.content if self.content else "None"
        tags = "; ".join(tag.value for tag in self.tags) if self.tags else "None"
        return f"Title: {title}, Content: {content}, Tags: {tags}"

    def get_display_data(self) -> tuple:
        """Returns title, content, and tags (as strings)"""
        title = self.title.value
        content = self.content
        tags = [tag.value for tag in self.tags]
        return title, content, tags


class NotesBook:
    def __init__(self) -> None:
        self.data = {}

    def __str__(self) -> str:
        return "\n".join(str(note) for note in self.data.values())

    def __iter__(self):
        return iter(self.data.values())

    @input_error 
    def add_note(self, note: Note) -> None:
        self.data[note.title.value] = note

    # what returns??
    @input_error  # will trigger ModuleNotFound error if run from here ???
    def find_note(self, title: str) -> dict:
        if title in self.data:
            return self.data[title]
        return None

    @input_error  # will trigger ModuleNotFound error if run from here ???
    def delete_note(self, title: str) -> None:
        # check if title still in data
        if title in self.data:
            del self.data[title]
            # return f"Note {title} has been deleted"
        else:
            raise ValueError(f"Record {title} is not found")

    def __str__(self) -> str:
        return "\n".join(str(note) for note in self.data)
