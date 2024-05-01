"""The authorization library for Discord Snipe Bot."""
# Imports
import json
import os.path

# Classes
class Auth:
    def load(self):
        """Loads the latest content from the database from machine local storage."""
        # Generate config.json file if its missing.
        if not os.path.isfile("config.json"):
            with open("config.json", 'x', encoding="utf-8") as f:
                json.dump({"auth": {"token": ""}, "config": {"owner_name": "", "logs": {"snipe": True, "editsnipe": True}}}, f)
                f.close()
        
        # Load config.json database
        with open("config.json", 'r', encoding="utf-8") as f: config = json.load(f)
        return config

    def save(self, data: dict):
        """Dumps all cached content from memory into local storage."""
        with open("config.json", 'w+', encoding="utf-8") as f: json.dump(data, f, indent=4)

    def initial_setup(self):
        """Runs the bot's initial setup by generating a `config.json` file if missing, and asking for bot token/owner username if not provided."""
        config = self.load()
        if config["auth"]["token"] == "":
            confirmation = input("[!] No bot token was detected in config.json. Would you like to input a token? (Y/n): ")
            if confirmation.lower() == "yes" or confirmation.lower() == "y":
                tkn = input("[>] Enter your Discord bot token: ")
                config["auth"]["token"] = str(tkn)
        if config["config"]["owner_name"] == "":
            confirmation = input("[!] No owner name was detected in config.json. Would you like to add one? (Y/n): ")
            if confirmation.lower() == "yes" or confirmation.lower() == "y":
                uname = input("[>] Enter your Discord username: ")
                config["config"]["owner_name"] = str(uname)
        self.save(config)

    def get_token(self) -> str:
        """Returns the token stored in `config.json`."""
        config = self.load()
        return config["auth"]["token"]

    def get_owner_name(self) -> str:
        """Returns the owner's name as `str` from `config.json`."""
        config = self.load()
        return config["config"]["owner_name"]
    
    def get_raw(self) -> dict:
        """Returns all of the raw `dict` content of the `config.json` database."""
        config = self.load()
        return config
