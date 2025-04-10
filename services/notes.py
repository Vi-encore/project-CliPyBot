# do you code here
# Maybe add function edit_note, that will show note book, ask what note you would like to edit (by title), and than will ask which part of note to edit (title, content or tags possibly)
from data.state import notes
from decorators.decorators import input_error, check_arguments
from models.note import Note
from helpers.helpers import save_notes