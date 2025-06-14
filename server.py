# server.py
from mcp.server.fastmcp import FastMCP
from datetime import datetime
import os

# Create an MCP server
mcp = FastMCP("AI ToDos")

FOLDER_NAME = "Data"
FOLDER_PATH = os.path.join(os.path.dirname(__file__), FOLDER_NAME)
os.makedirs(FOLDER_PATH, exist_ok=True)
SAVED_DATA = os.path.join(FOLDER_PATH, "saved_data.txt")

# Helper function for ensuring that file for storing data exists
def ensure_file_exists():
    if not os.path.exists(SAVED_DATA):
        with open(SAVED_DATA, "w") as f:
            f.write("")

# Add-ToDo Tool
@mcp.tool()
def add_todo(message: str) -> str:
    """
    Add a new ToDo/note to the data storage file.

    Args:
        message (str): The ToDo/note content to be added.
    
    Returns:
        str: Confirmation message indicating the note has been saved.
    """
    ensure_file_exists()

    # Log data (Time & Date)
    curr_time = datetime.now()
    timestamp_str = curr_time.strftime("%Y-%m-%d %H:%M:%S") + ": "

    with open(SAVED_DATA, "a") as f:
        f.write(timestamp_str + message + "\n")

    return "ToDo saved!"

# Read-ToDo Tool
@mcp.tool()
def read_notes() -> str:
    """
    Read all saved ToDos/notes and return the corresponding information. 
    If only asked for one, return the correct/required ToDo.
    If asked to summarize, return a summarization of the corresponding ToDos.
    If asked about a specific day/time, return the corresponding ToDos.
    
    Returns:
        str: Required ToDo(s) as a single string seperated by line breaks.
        If no notes exist, return a default message.
    """
    ensure_file_exists()

    with open(SAVED_DATA, "r") as f:
        content = f.read().strip()

    return content or "ToDo list is empty."

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
    ensure_file_exists()
    with open(SAVED_DATA, "r") as f:
        content = f.read().strip()
    if not content:
        return "ToDo list is empty."

    return f"Summarize the current ToDos: {content}"

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting in the context of ToDos/notes"""
    return f"Hello, {name}. Do you want to get an overview of your ToDos?"

if __name__ == "__main__":
    print(SAVED_DATA)