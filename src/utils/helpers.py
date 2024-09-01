"""Helpers"""

from datetime import datetime
import traceback


def print_error(message_error: str):
    """Print error function

    Args:
        message_error (str): error message
    """
    message_error = "[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + message_error
    print(message_error)
    with open("error.txt", mode="a", encoding="utf-8") as error_file:
        error_file.write(message_error)
        error_file.write(traceback.format_exc())
