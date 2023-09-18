from termcolor import colored

def print_with_color(message, color, prefix=""):
    print(colored(f"{prefix} {message}", color))