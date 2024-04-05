# Imports
from datetime import datetime

# Classes and Functions
class Logger:
    """A class used for logging important new snipe and editsnipe entries, as well as errors."""
    def __init__(self):
        start_timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{start_timestamp}] Logging initialized.")

    def snipe(self, text: str):
        """Logs a sniped message to log file."""
        with open("logs/snipe.log", 'a', encoding="utf-8") as file:
            # timestamp = datetime.now().strftime("%H:%M:%S")  Disable internal timestamp logging
            file.write(f"{text}\n")
            file.close()

    def editsnipe(self, text: str):
        """Logs an edited message to log file."""
        with open("logs/editsnipe.log", 'a', encoding="utf-8") as file:
            # timestamp = datetime.now().strftime("%H:%M:%S")  Disable internal timestamp logging
            file.write(f"{text}\n")
            file.close()

    def error(self, text: str):
        """Logs an error message to log file."""
        with open("logs/errors.log", 'a', encoding="utf-8") as file:
            # timestamp = datetime.now().strftime("%H:%M:%S")  Disable internal timestamp logging
            file.write(f"{text}\n")
            file.close()
