import os
import json

FOLDER_PATH = os.path.join(os.path.dirname(__file__), "Data")
os.makedirs(FOLDER_PATH, exist_ok=True)
DATA_FILE = os.path.join(FOLDER_PATH, "todos.json")

def ensure_file_exists():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

def load_todos():
    ensure_file_exists()
    with open(DATA_FILE, "r") as f:
        return json.load(f)
    
def save_todos(todos):
    with open(DATA_FILE, "w") as f:
        json.dump(todos, f, indent=2)