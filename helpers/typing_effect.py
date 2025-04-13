import time
from rich.console import Console

console = Console()

# MAKE TYPING EFFECT 
def typing_effect(text, color='sea_green3', s_style='normal'):
    """ Function to mimic typing effect in the console with customizable color and style """
    for char in text:
        style = f"{color}"  # Initialize with color
        if s_style != 'normal':
            style += f" {s_style}"  # Add style if it's not 'normal'
        console.print(f"{char}", style=style, end='', no_wrap=True)
        time.sleep(0.022)
    # console.print()  # To move to the next line after printing the whole text

# TYPING EFFECT FOR INPUT 
def typing_input(prompt, color='sea_green3', s_style='normal'):
    """ Mimic typing effect for input prompt with customizable color and style """
    typing_effect(prompt, color, s_style)
    return console.input()  # Collect user input after the typing effect

# TYPING EFFECT FOR OUTPUT
def typing_output(output, color='green', s_style='bold'):
    """ Mimic typing effect for any printed output with customizable color and style """
    typing_effect(output, color, s_style)
    console.print()  # To move to the next line after printing the whole text
   
   
   