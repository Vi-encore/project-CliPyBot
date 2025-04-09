import os
import time
import random
import string

from colorama import init, Fore, Back, Style
init(autoreset=True)

class MatrixColumn:
    def __init__(self, rows=10):
        """
        Represents one column of falling characters. Each column spawns
        random characters which move downward.
        """
        self.falling_chars = []
        self.chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        self.rows = rows

    def update(self):
        """
        Moves all characters down one row. Removes any that pass 'end_line'.
        Spawns a new character at row=0 (top) with a random vanish line.
        """
        for fc in self.falling_chars:
            fc['line'] += 1

        self.falling_chars = [fc for fc in self.falling_chars if fc['line'] <= fc['end_line']]

        new_char = random.choice(self.chars)
        end_line = random.randint(self.rows - 5, self.rows - 1)
        self.falling_chars.append({
            'char': new_char,
            'line': 0,
            'end_line': end_line
        })

    def get_display_line(self, total_lines=10):
        """
        Returns a list of length 'total_lines'. Each element is a character
        at that row or a space ' ' if none is present.
        """
        display = [" "] * total_lines
        for fc in self.falling_chars:
            if 0 <= fc['line'] < total_lines:
                display[fc['line']] = fc['char']
        return display

def matrix_drop(duration=7, rows=20, columns=100):
    """
    Runs the matrix animation for 'duration' seconds, overlaying static text
    that only appears once a falling character "arrives" at each letter's position.
    """

    # Define the text lines and positions (row, col)
    def build_static_positions():
        text_map = {}
        
        def place_text(row, col, text):
            for i, ch in enumerate(text):
                text_map[(row, col + i)] = ch

        # Lines (0-based indexing):
        place_text(3,  10, " Project was developed by ")
        place_text(5,  50, " Neo Dev Group ")
        place_text(7,  20, " Victoria Mariushko ")
        place_text(10, 70, " Olena Badum ")
        place_text(13, 50, " Oleksandr Sorochynskyi ")
        place_text(14, 10, " Eduard Bolma ")

        return text_map

    static_positions = build_static_positions()

    # Track whether each letter's position has "arrived" yet
    arrived_positions = {pos: False for pos in static_positions}

    start_time = time.time()

    # Create columns, each with a random update speed
    cols = []
    for _ in range(columns):
        col = MatrixColumn(rows=rows)
        col.update_interval = random.uniform(0.1, 0.3)
        col.last_update = time.time()
        cols.append(col)

    while time.time() - start_time < duration:
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')

        current_time = time.time()
        # Update columns whose interval is due
        for col in cols:
            if current_time - col.last_update >= col.update_interval:
                col.update()
                col.last_update = current_time

        # Build and print each row
        for row_idx in range(rows):
            row_chars = []
            for col_idx, col in enumerate(cols):
                c = col.get_display_line(rows)[row_idx]

                if (row_idx, col_idx) in static_positions:
                    # If this position is part of our static text
                    if not arrived_positions[(row_idx, col_idx)] and c != " ":
                        arrived_positions[(row_idx, col_idx)] = True

                    if arrived_positions[(row_idx, col_idx)]:
                        # Show with a green background and white foreground
                        c = (
                            Style.BRIGHT        # Make it bold/bright
                            + Back.GREEN        # Green background
                            + Fore.WHITE        # White foreground
                            + static_positions[(row_idx, col_idx)]
                            + Style.RESET_ALL
                        )

                        row_chars.append(c)
                    else:
                        # Not arrived yet => normal random character in green
                        row_chars.append(Fore.GREEN + c + Style.RESET_ALL)
                else:
                    # Normal random char in green
                    row_chars.append(Fore.GREEN + c + Style.RESET_ALL)

            # Print the row
            print("".join(row_chars))

        # Small delay for animation pacing
        time.sleep(0.01)
