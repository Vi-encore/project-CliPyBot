from rich.console import Console
from helpers.typing_effect import typing_output
from typing import Literal

console = Console()  # Initialize Console for rich output


# Exception handler for input errors
def input_error(func):
    """
    Decorator to handle input-related exceptions for a function.

    Catches common exceptions such as KeyError, ValueError, IndexError,
    or general exceptions during the execution of a function.
    Displays appropriate error messages using `typing_output`.

    Args:
        func (function): The function to wrap with the exception handler.

    Returns:
        function: The wrapped function with error handling logic.
    """

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
    """
    Decorator to check if a function is called with a minimum number of arguments.

    Raises a ValueError if the number of arguments provided is less than the specified
    minimum. Displays an error message using `typing_output`.

    Args:
        min_args (int): The minimum number of arguments required.

    Returns:
        function: A decorator wrapping the target function with argument validation.
    """

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


# Exception handler for class methods
def exception_handler(func):
    """
    Decorator to handle exceptions for class methods.

    Catches exceptions such as ValueError and displays an appropriate
    error message using `typing_output`. Ensures that any unhandled
    exception does not disrupt execution.

    Args:
        func (function): The class method to wrap with the exception handler.

    Returns:
        function: The wrapped class method with error handling logic.
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            typing_output(f"Error: {e} 🚨", color="red")
            return None

    return inner
