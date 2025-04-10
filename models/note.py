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
    def __init__(self):
        self.title = None
        self.content = None
        self.tags = []

    def __str__(self) -> str:
        return f"Title: {self.title.value}, content: {self.content.value}, tags: {', '.join(tag.value for tag in self.tags)}."

    # @input_error  # will trigger ModuleNotFound error if run from here ???
    def create_note(self):  # recursion
        try:

            def create_title():
                new_title = input("Enter a note title: ")
                if len(new_title) > 1000:
                    print("Error: Title length should not exceed 1000 symbols.")
                    try_again = input("Would you try again? (y/n): ").lower()
                    if try_again == "y":
                        return create_title()  # Recursive call if user wants to retry
                    else:
                        return None  # Exit without creating a title
                return Title(new_title)  # Return valid Title instance

            self.title = create_title()
            if not self.title:
                return None

            def create_content():
                new_content = input("Enter note content: ")
                if len(new_content) > 20000:
                    print("Error: Content length should not exceed 20000 symbols.")
                    try_again = input("Would you try again? (y/n): ").lower()
                    if try_again == "y":
                        return create_content()  # Recursive call if user wants to retry
                    else:
                        return None  # Exit without creating a title
                return Content(new_content)  # Return valid Title instance

            self.content = create_content()
            if not self.content:
                return None

            def create_tags():
                tags_input = input("Enter your tag(s), separated by commas: ").split(
                    ","
                )
                tags = [tag.strip() for tag in tags_input]

                if len(tags) > 10:
                    print("Error: You cannot enter more than 10 tags.")
                    try_again = input("Would you try again? (y/n): ").lower()
                    if try_again == "y":
                        return create_tags()
                    else:
                        return []

                for tag in tags:
                    if len(tag) > 25:
                        print(f"Error: Tag {tag} exceeds 25 characters")
                        try_again = input("Would you try again? (y/n): ").lower()
                        if try_again == "y":
                            return create_tags()
                        else:
                            return []
                return [Tag(tag) for tag in tags]

            create_tag = input("Want to add a tag? (y/n): ").lower()
            new_tags = []
            if create_tag == "y":
                new_tags = create_tags()

            self.tags = new_tags
            return self  # Return the updated instance
        except ValueError as e:
            print(f"Error: {e}")
            return None  # Return None in case of an error

    def edit_content(self):
        try:
            is_change = input(
                f"Do you want to change the content '{self.content.value}' for the note titled '{self.title.value}'? (y/n): "
            ).lower()
            if is_change == "y":
                new_content = input("Enter new content for this note: ")
                if len(new_content) > 20000:
                    print("Content length should not exceed 20000 symbols.")
                else:
                    self.content.value = new_content
                    print(f"The content for '{self.title.value}' has been updated.")
            else:
                print("No changes were made.")
        except AttributeError:
            print("Error: The note doesn't have content or a title set.")

    def edit_title(self):
        try:
            is_change = input(
                f"Do you want to change the title '{self.title.value}' for the note'? (y/n): "
            ).lower()
            if is_change == "y":
                new_title = input("Enter new title for this note: ")
                if len(new_title) > 1000:
                    print("Title length should not exceed 1000 symbols.")
                else:
                    self.title.value = new_title
                    print(f"The '{self.title.value}'  has been updated.")
            else:
                print("No changes were made.")
        except AttributeError:
            print("Error: The note doesn't have content or a title set.")

    def edit_tags(self):
        try:
            # Display current tags without the `#` prefix
            is_change = input(
                f"Do you want to change the tags for '{self.title.value}' note'? (y/n): "
            ).lower()

            if is_change == "y":
                tags_to_edit = [
                    tag.value[1:] for tag in self.tags
                ]  # Remove the `#` prefix
                print(f"Current tags: {', '.join(tags_to_edit)}")

                # Ask the user if they want to edit all or specific tags
                action = input(
                    "Do you want to edit all tags or specific ones? (all/specific): "
                ).lower()

                if action == "all":
                    while True:
                        new_tags = input(
                            "Enter new tags, separated by commas: "
                        ).strip()
                        if not new_tags:  # Check if the input is empty
                            print("You did not enter any value.")
                            try_again = input(
                                "Would you like to try again? (y/n): "
                            ).lower()
                            if try_again != "y":
                                print("Tags have not been changed.")
                                return
                        else:
                            self.tags = [
                                Tag(tag.strip()) for tag in new_tags.split(",")
                            ]  # Add `#` prefix automatically
                            break
                elif action == "specific":
                    while True:
                        for index, tag in enumerate(tags_to_edit, 1):
                            print(f"{index}. {tag}")
                        tag_indices = input(
                            "Enter the numbers of tags you want to edit:"
                        ).strip()
                        if not tag_indices:  # Check if the input is empty
                            print("You did not enter any value.")
                            try_again = input(
                                "Would you like to try again? (y/n): "
                            ).lower()
                            if try_again != "y":
                                print("Tags have not been changed.")
                                return
                        else:
                            tag_indices = [
                                int(index) - 1
                                for index in tag_indices.split(",")
                                if index.isdigit()
                            ]  # Convert to zero-based indices
                            for i in tag_indices:
                                if 0 <= i < len(tags_to_edit):  # Ensure valid index
                                    while True:
                                        new_tag = input(
                                            f"Enter new value for tag '{tags_to_edit[i]}': "
                                        ).strip()
                                        if (
                                            not new_tag
                                        ):  # Check if input for new tag is empty
                                            print("You did not enter any value.")
                                            try_again = input(
                                                "Would you like to try again? (y/n): "
                                            ).lower()
                                            if try_again != "y":
                                                print(
                                                    f"No changes were made to the tag '{tags_to_edit[i]}'."
                                                )
                                                break
                                        else:
                                            self.tags[i] = Tag(
                                                new_tag
                                            )  # Update the tag
                                            break
                            break
                else:
                    print("No changes were made to the tags.")

                # Confirm updates
                updated_tags = ", ".join(tag.value for tag in self.tags)
                print(f"Updated tags: {updated_tags}")
        except AttributeError:
            print("Error: The note doesn't have content or a title set.")


class NotesBook(UserDict):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "\n".join(str(note) for note in self.data.values())

    def add_note(self, note: Note):
        if (
            note and note.title and note.content
        ):  # Ensure note has valid title and content
            self.data[note.title.value] = note
            return f"Note with title '{note.title.value}' has been added."
        else:
            return "Failed to add note. Ensure the note has a title and content."

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
book = NotesBook()
# note = Note()
# created_note = (
#     note.create_note()
# )  ated_note)# Ensure create_note() returns the `self` Note instance
# book.add_note(cre
# second_note = Note().create_note()
# book.add_note(second_note)
book.add_note(Note().create_note())
# book.add_note(Note().create_note())

print(book)

# Edit the content of the note
# title = created_note.title.value
to_edit = book.find_note("title2")

print(book)

# book.delete_note("title1")


# to_edit.edit_title()
to_edit.edit_tags()

print(book)

# print(edited_note)

# print(result)
# print(book.find_note(second_note.title.value))
# Display all notes in the NotesBook
# print(book)
