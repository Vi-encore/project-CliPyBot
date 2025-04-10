from rich.console import Console
from helpers.typing_effect import typing_output

console = Console()  # Initialize Console for rich output


# Eception handler for input errors
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            typing_output(f"Error: KeyError occurred: {e} 🚨", color="red")
            return 1
        except ValueError as e:
            typing_output(f"Error: ValueError occurred: {e} 🚨", color="red")
            return 1
        except IndexError as e:
            typing_output(f"Error: IndexError occurred: {e} 🚨", color="red")
            return 1
        except Exception as e:
            typing_output(f"Error: {e} 🚨", color="red")
            return 1

    return inner


# Check length of arguments during input
def check_arguments(min_args: int):
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                if len(args) < min_args:
                    raise ValueError(f"Please provide at least {min_args} arguments")
            except ValueError as e:
                typing_output(f"Error: ValueError {e} 🚨", color="red")
                return 1
            return func(*args, **kwargs)

        return inner

    return decorator


# Exception handler for ClASS methods
def exception_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            typing_output(f"Error: {e} 🚨", color="red")
            return None

    return inner
