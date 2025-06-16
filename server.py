# server.py
import os
import json
import uuid
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("MCP ToDos")

FOLDER_PATH = os.path.join(os.path.dirname(__file__), "Data")
os.makedirs(FOLDER_PATH, exist_ok=True)
DATA_FILE = os.path.join(FOLDER_PATH, "todos.json")

# Helper function for ensuring that file for storing data exists
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

# Tool: Add ToDos
@mcp.tool()
def add_todo(message: str) -> str:
    """
    Add a new ToDo/note to the data storage file.

    Args:
        message (str): The ToDo/note content to be added.
    
    Returns:
        str: Confirmation message indicating the note has been saved.
    """
    todos = load_todos()
    new_todo = {
        "id": uuid.uuid4().hex[:8],
        "message": message,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "done": False,
        "done_at": None
    }

    todos.append(new_todo)
    save_todos(todos)
    return f"ToDo added with ID {new_todo['id']}."

# Tool: Show ToDos
@mcp.tool()
def list_todos(only_open: bool = False) -> str:
    """
    Read all saved ToDos/notes and return the corresponding information. 
    If only asked for one, return the correct/required ToDo.
    If asked to summarize, return a summarization of the corresponding ToDos.
    If asked about a specific day/time, return the corresponding ToDos.
    
    Returns:
        str: Required ToDo(s) as a single string seperated by line breaks.
        If no notes exist, return a default message.
    """
    todos = load_todos()
    filtered = [todo for todo in todos if not todo["done"]] if only_open else todos
    if not filtered:
        return "No ToDos found."
    
    return "\n".join(f"[{'x' if t['done'] else ' '}] ({t['id']}) {t['message']} – {t['created_at']}" for t in filtered)

# Tool: Mark ToDo as done
@mcp.tool()
def mark_done(todo_id: str) -> str:
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            if todo["id"] == todo_id:
                if todo["done"]:
                    return "ToDo is already marked as done."
                todo["done"] = True
                todo["done_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_todos(todos)

                return f"ToDo {todo_id} marked as done."
    return f"No ToDo found with ID {todo_id}."

# Tool: Delete ToDo
@mcp.tool()
def delete_todo(todo_id: str) -> str:
    todos = load_todos()
    new_todos = [todo for todo in todos if todo["id"] != todo_id]

    if len(new_todos) == len(todos):
        return f"No ToDo found with ID {todo_id}."
    
    save_todos(new_todos)

    return f"ToDo {todo_id} deleted."

# Custom prompt
@mcp.prompt()
def note_summary_prompt() -> str:
    """
    Generate a prompt asking the AI to summarize all current ToDos/notes.

    Returns:
        str: A prompt string that includes all important ToDos/notes and
         asks for a summary.
        If no notes exist, a message will be shown indicating that.
    """
    todos = load_todos()
    if not todos:
        return "There are no ToDos to summarize."
    
    text = "\n".join(f"{'[x]' if t['done'] else '[ ]'} {t['message']}" for t in todos)
    
    return f"Summarize the following ToDos:\n{text}"

# Resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hi {name}, would you like to manage your ToDos now?"

if __name__ == "__main__":
    print("ToDo system initialized at:", DATA_FILE)