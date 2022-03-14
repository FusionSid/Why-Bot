import logging
import sys
import traceback

def log_errors(type, value, tb):
    logging.basicConfig(filename="log/logs.txt", format='[%(levelname)s] (%(asctime)s) - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    error = f"{type.__name__}:\n\tTraceback (most recent call last):\n\t{'    '.join(traceback.format_tb(tb))}\n\t{value}"
    logging.error(error)

    # Commenting out this line will stop errors being printed to console
    sys.__excepthook__(type, value, tb)

sys.excepthook = log_errors