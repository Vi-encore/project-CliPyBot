from datetime import datetime


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

    #     self.notes = {}
    # self.title = Title(title)
    # self.content = Content(content)
    # self.tag = None

    def __str__(self) -> str:
        # print(self.title.value)
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
        return str(self)


note = Note()
# print(note.create_note())
created_note = note.create_note()
print(created_note)


# class NotesBook():
#   def __init__(self):
#     self.data = {}

#   def add_note(self, note: Note):
#     self.data[note.title.value] = Note(note)


# book = NotesBook()
# book.add_note('')
