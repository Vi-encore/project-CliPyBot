# CliPyBot

A **multifunctional Python bot** designed to efficiently manage your contacts and notes. Seamlessly add, edit and organize personal information while keeping track of upcoming birthdays and your essential notes.

## Features

### Contact Management:

- Effortlessly add contacts with details like phone, email, address, and birthday.
- Edit or update contact information as needed.
- Delete contacts you no longer need.
- Display detailed information for a specific contact.
- View a list of all stored contacts at a glance.
- Keep track of upcoming birthdays by specifying a date range.
- Expand contact entries by adding more information over time.
- Export all contacts to a CSV file for easy backup or sharing.

### Note-Taking:

- Create new notes with titles, content, and tags for easy organization.
- Edit existing notes to update information.
- Search notes using specific keywords.
- List all available notes at any time.
- Show details of a selected note.
- Delete notes you no longer need.
- Export notes to a CSV file for external use or backup.

### General Features:

- Interactive greetings when the bot is started.
- A comprehensive help command listing all available features and instructions.
- Smoothly close the bot while ensuring all data is saved securely.
- A playful "goodbye" sequence with a unique effect for added fun.

## Installation

### Requirements:

- Python 3.12+

**1. Clone this repository**:

```bash
git clone https://github.com/Vi-encore/project-CliPyBot.git
```

**2. Navigate to youe project directory:**

```bash
cd project-CliPyBot
```

**3. Set Up a Virtual Environment:**

- for Windows:
  ```bash
  python -m venv .venv
  .\.venv\Scripts\activate
  ```
- for MacOS/Linux:

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

**4. Install required dependencies:**

```bash
pip install -r requirements.txt
```

## Usage

Run the bot

```bash
python main.py
```

### Contact management commands:

- **add contact**: Adds a new contact with details like phone, email, address, and birthday.
- **find contact**: Finds a contact by name.
- **all contacts**: Displays a list of all stored contacts.
- **all birthdays**: Shows all upcoming birthdays within a specified number of days.
- **edit contact**: Edits details for an existing contact.
- **delete contact**: Deletes an existing contact from the list.
- **expand contact**: Adds additional information to an existing contact.
- **show contact**: Displays detailed information for a specific contact.
- **export contacts**: Exports all contacts to a CSV file for easy backup or sharing.

### Note-Taking Commands:

- **all notes**: Lists all existing notes.
- **add note**: Creates a new note with a title and content.
- **find note**: Finds a note using a keyword search.
- **change note**: Updates the content or tags of an existing note.
- **delete note**: Removes a specific note from the database.
- **export notes**: Exports all notes to a CSV file.
- **show note**: Displays the details of a specific note.

### General Commands:

- **hello**: Greets the user.
- **help**: Shows a list of all available commands.
- **close/exit/quit**: Closes the bot and saves all data.
- **goodbye**: Closes the bot with a special effect (e.g., matrix drop animation).

## Contributing

We welcome contributions. Here's how get involved:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a description of your changes.

## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License, allowing you to use and modify it freely.
