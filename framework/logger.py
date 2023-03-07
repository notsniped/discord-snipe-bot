# Imports
import os
import os.path
import datetime

# Variables
homedir = os.getcwd()

# Classes and Functions
class Logger:
    """A class used for logging important information and alerts."""
    def __init__(self, os_name: str, directory: str):
        self.os_name = os_name
        self.directory = directory
        start_timestamp = datetime.time().strftime('%H:%M:%S')
        print(f"[{start_timestamp}] Logging initialized.")

    def snipe(self, text: str):
        """Logs a sniped message to log file."""
        if os.name == "nt":
            with open(f"{homedir}\\snipe-bot-data\\snipe.log", 'w+', encoding="utf-8") as file:
                # timestamp = datetime.now().strftime("%H:%M:%S")  Disable internal timestamp logging
                file.write(f"{text}\n")
                file.close()
        elif os.name == "posix":
            with open(f"{homedir}/snipe-bot-data/snipe.log", 'w+', encoding="utf-8") as file:
                # timestamp = datetime.now().strftime("%H:%M:%S")  Disable internal timestamp logging
                file.write(f"{text}\n")
                file.close()

    def editsnipe(self, text: str):
        """Logs an edited message to log file."""
        if os.name == "nt":
            with open(f"{homedir}\\snipe-bot-data\\editsnipe.log", 'w+', encoding="utf-8") as file:
                # timestamp = datetime.now().strftime("%H:%M:%S")  Disable internal timestamp logging
                file.write(f"{text}\n")
                file.close()
        elif os.name == "posix":
            with open(f"{homedir}/snipe-bot-data/editsnipe.log", 'w+', encoding="utf-8") as file:
                # timestamp = datetime.now().strftime("%H:%M:%S")  Disable internal timestamp logging
                file.write(f"{text}\n")
                file.close()

    def error(self, text: str):
        """Logs an error message to log file."""
        if os.name == "nt":
            with open(f"{homedir}\\snipe-bot-data\\errors.log", 'w+', encoding="utf-8") as file:
                # timestamp = datetime.now().strftime("%H:%M:%S")  Disable internal timestamp logging
                file.write(f"{text}\n")
                file.close()
        elif os.name == "posix":
            with open(f"{homedir}/snipe-bot-data/errors.log", 'w+', encoding="utf-8") as file:
                # timestamp = datetime.now().strftime("%H:%M:%S")  Disable internal timestamp logging
                file.write(f"{text}\n")
                file.close()
