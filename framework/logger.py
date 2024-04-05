# Imports
import os
import os.path
import datetime

# Classes and Functions
class Logger:
    def __init__(self, os_name: str, directory: str):
        self.os_name = os_name
        self.directory = directory
    """A class used for logging important new snipe and editsnipe entries, as well as errors."""
        start_timestamp = datetime.time().strftime('%H:%M:%S')
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
