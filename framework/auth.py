# Imports
import json

# Variables
with open("config.json", 'r', encoding="utf-8") as f: config = json.load(f)

# Functions
def get_token() -> str:
    """Returns the token stored in the config.json database file."""
    return config["auth"]["token"]
