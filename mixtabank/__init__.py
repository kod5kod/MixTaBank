import json
import os

# Define the path to the JSON configuration file
UCI_DICT_FILE_PATH = os.path.join(os.path.dirname(__file__), "data_src_dict", "UCI.JSON")

# Load the UCI JSON data
try:
    with open(UCI_DICT_FILE_PATH, "r", encoding="utf-8") as f:
        uci_dict = json.load(f)
except FileNotFoundError:
    uci_dict = {}  # Or handle the error as needed, e.g., load default config
    print(f"Error: FileNotFoundError {UCI_DICT_FILE_PATH}")
except json.JSONDecodeError:
    uci_dict = {}  # Handle invalid JSON format
    print(f"Error: Invalid JSON in {UCI_DICT_FILE_PATH}")


