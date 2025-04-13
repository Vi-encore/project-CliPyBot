from decorators.decorators import input_error
from typing import Iterator


class Field:
    """
    Base class for all fields in the notes.

    Attributes:
        value: The value stored in the field.
    """

    def __init__(self, value) -> None:
        """
        Initialize a Field object.

        Args:
            value: The value to be stored in the field.
        """
        self.value = value

    def __str__(self) -> str:
        """
        Return string representation of the field.

        Returns:
            str: String representation of the field value.
        """
        return str(self.value)


class Title(Field):
    """
    Field for storing note titles.

    Inherits from Field class.
    """

    def __init__(self, title: str) -> None:
        """
        Initialize a Title object.

        Args:
            title (str): The title to be stored.
        """
        super().__init__(title)


class Content(Field):
    """
    Field for storing note content.

    Inherits from Field class.
    """

    def __init__(self, content: str) -> None:
        """
        Initialize a Content object.

        Args:
            content (str): The content to be stored.
        """
        super().__init__(content)


class Tag(Field):
    """
    Field for storing note tags with formatting.

    Inherits from Field class.
    """

    def __init__(self, tag: str) -> None:
        """
        Initialize a Tag object with formatting.

        Args:
            tag (str): The tag to be stored and formatted.
        """
        tag = self.create_tag(tag.strip())
        super().__init__(tag)

    @staticmethod
    def create_tag(tag: str) -> str:
        """
        Format tag by adding a hashtag and replacing spaces with underscores.

        Args:
            tag (str): The tag to be formatted.

        Returns:
            str: Formatted tag.
        """
        tag = f"#{tag.replace(' ', "_")}"
        return tag


class Note:
    """
    Class representing a note with title, content, and tags.

    Provides methods for managing note contents and tags.
    """

    def __init__(self, title: str) -> None:
        """
        Initialize a Note object with a title.

        Args:
            title (str): The title of the note.
        """
        self.title = Title(title)
        self.content = None
        self.tags = []

    @input_error
    def add_tag(self, tag: str) -> None:
        """
        Add a tag to the note.

        Args:
            tag (str): The tag to add.

        Raises:
            ValueError: If maximum tags limit exceeded or tag length is invalid.
        """
        if len(self.tags) < 10 and len(tag) <= 25:
            self.tags.append(Tag(tag))
        else:
            raise ValueError("Maximum tags limit exceeded or tag length is invalid.")

    def delete_tag(self, tag: str) -> bool:
        """
        Delete a tag from the note.

        Args:
            tag (str): The tag to delete.

        Returns:
            bool: True if tag was successfully deleted.

        Raises:
            ValueError: If the tag is not found.
        """
        for t in self.tags:
            if t.value == tag:
                self.tags.remove(t)
                return True
        raise ValueError(f"Tag '{tag}' not found.")

    @input_error
    def edit_tag(self, old_tag: str, new_tag: str) -> None:
        """
        Edit a tag in the note.

        Args:
            old_tag (str): The tag to edit.
            new_tag (str): The new tag value.

        Raises:
            ValueError: If the tag is not found.
        """
        for i, tag in enumerate(self.tags):
            if tag.value == old_tag:
                self.tags[i] = Tag(new_tag)
                return
        raise ValueError(f"Tag '{old_tag}' not found.")

    @input_error
    def find_tag(self, tag: str) -> Tag | None:
        """
        Find a tag in the note's tags.

        Args:
            tag (str): The tag to find.

        Returns:
            Tag or None: The Tag object if found, None otherwise.
        """
        for t in self.tags:
            if t.value == tag:
                return t
        return None

    @input_error
    def edit_content(self, new_content: str) -> None:
        """
        Edit the content of the note.

        Args:
            new_content (str): The new content.

        Raises:
            ValueError: If content length exceeds 20000 characters.
        """
        if len(new_content) <= 20000:
            self.content = new_content
        else:
            raise ValueError("Content length should not exceed 20000 characters.")

    @input_error
    def add_content(self, content: str) -> None:
        """
        Add content to the note.

        Args:
            content (str): The content to add.

        Raises:
            ValueError: If content format is invalid.
        """
        self.content = Content(content).value

    def delete_content(self) -> None:
        """
        Delete the content of the note.
        """
        self.content = ""

    @input_error
    def edit_title(self, new_title: str) -> None:
        """
        Edit the title of the note.

        Args:
            new_title (str): The new title.

        Raises:
            ValueError: If title length exceeds 1000 characters.
        """
        if len(new_title) <= 1000:
            self.title = new_title
        else:
            raise ValueError("Title length should not exceed 1000 characters.")

    def __str__(self) -> str:
        """
        Return string representation of the note.

        Returns:
            str: String representation of the note with title, content, and tags.
        """
        title = self.title if self.title else "None"
        content = self.content if self.content else "None"
        tags = "; ".join(tag.value for tag in self.tags) if self.tags else "None"
        return f"Title: {title}, Content: {content}, Tags: {tags}"

    def get_display_data(self) -> tuple:
        """
        Get display data for the note.

        Returns:
            tuple: A tuple containing title, content, and tags list.
        """
        title = self.title.value
        content = self.content
        tags = [tag.value for tag in self.tags]
        return title, content, tags


class NotesBook:
    """
    Class representing a collection of notes.

    Provides methods for adding, finding, and managing notes.
    """

    def __init__(self) -> None:
        """
        Initialize a NotesBook object.
        """
        self.data = {}

    def __str__(self) -> str:
        """
        Return string representation of the notes book.

        Returns:
            str: String representation of all notes in the book.
        """
        return "\n".join(str(note) for note in self.data.values())

    def __iter__(self) -> Iterator:
        """
        Make the NotesBook iterable.

        Returns:
            iterator: Iterator over the notes in the book.
        """
        return iter(self.data.values())

    @input_error
    def add_note(self, note: Note) -> None:
        """
        Add a note to the notes book.

        Args:
            note (Note): The note to add.

        Raises:
            ValueError: If the note format is invalid.
        """
        self.data[note.title.value] = note

    @input_error
    def find_note(self, title: str) -> Note | None:
        """
        Find a note by title.

        Args:
            title (str): The title to search for.

        Returns:
            Note or None: The matching note if found, None otherwise.

        Raises:
            ValueError: If the title format is invalid.
        """
        if title in self.data:
            return self.data[title]
        return None

    @input_error
    def delete_note(self, title: str) -> None:
        """
        Delete a note from the notes book.

        Args:
            title (str): The title of the note to delete.

        Raises:
            ValueError: If the note is not found.
        """
        if title in self.data:
            del self.data[title]
        else:
            raise ValueError(f"Record {title} is not found")

    @input_error
    def search(
        self, query: str, by_title=False, by_tag=False, by_content=False
    ) -> list:
        """
        Search for notes matching a query.

        Args:
            query (str): The search query.
            by_title (bool, optional): Search by title. Defaults to False.
            by_tag (bool, optional): Search by tag. Defaults to False.
            by_content (bool, optional): Search by content. Defaults to False.

        Returns:
            list: List of matching notes.

        Raises:
            ValueError: If the query format is invalid.
        """
        query = query.strip().lower()
        results = []

        for key, note in self.data.items():
            if by_title and query in key.strip().lower():
                results.append(note)
            elif by_tag and any(query in tag.value.lower() for tag in note.tags):
                results.append(note)
            elif by_content and note.content and query in note.content.lower():
                results.append(note)

        return results

    def __str__(self) -> str:
        """
        Return string representation of the notes book.

        Returns:
            str: String representation of all notes in the book.
        """
        return "\n".join(str(note) for note in self.data)
