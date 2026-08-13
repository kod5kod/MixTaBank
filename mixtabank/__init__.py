import json
import os

# Define the path to the JSON configuration files
UCI_DICT_FILE_PATH = os.path.join(os.path.dirname(__file__), "data_src_dict", "UCI.JSON")
KAGGLE_DICT_FILE_PATH = os.path.join(os.path.dirname(__file__), "data_src_dict", "Kaggle.JSON")

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
    
    
# Load the KAGGLE JSON data
try:
    with open(KAGGLE_DICT_FILE_PATH, "r", encoding="utf-8") as f:
        kaggle_dict = json.load(f)
except FileNotFoundError:
    kaggle_dict = {}  # Or handle the error as needed, e.g., load default config
    print(f"Error: FileNotFoundError {KAGGLE_DICT_FILE_PATH}")
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in {KAGGLE_DICT_FILE_PATH}")


from .src.loaders import dataset_loader, download_datasets, Dataset
from .src.splits import train_valid_test_split
from .src.metadata import get_df_info, get_metadata, generate_dataset_info_json
