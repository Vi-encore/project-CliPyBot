from colorama import Fore, Style

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            print(Fore.RED + f"Error: KeyError occurred: {e}" + Style.RESET_ALL)
            return 1
        except ValueError as e:
            print(Fore.RED + f"Error: ValueError occurred: {e}" + Style.RESET_ALL)
            return 1
        except IndexError as e:
            print(Fore.RED + f"Error: IndexError occurred: {e}" + Style.RESET_ALL)
            return 1
        except Exception as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
            return 1
    return inner

def check_arguments(min_args: int):
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                if len(args) < min_args:
                    raise ValueError(f"Please provide at least {min_args} arguments")
            except ValueError as e:
                print(Fore.RED + f"Error: ValueError {e}" + Style.RESET_ALL)
                return 1
            return func(*args, **kwargs)
        return inner
    return decorator

def exception_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(f"Error: {e}") 
            return None  
    return inner