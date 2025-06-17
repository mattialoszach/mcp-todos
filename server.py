import uuid
from datetime import datetime
from mcp.server.fastmcp import FastMCP
from utils import DATA_FILE, ensure_file_exists, load_todos, save_todos

# Create an MCP server
mcp = FastMCP("MCP ToDos")

# Tool: Add ToDos
@mcp.tool()
def add_todo(message: str) -> str:
    """
    Add a new ToDo item with a message and timestamp.

    Use this when the user wants to create a new task or reminder.
    The ToDo is stored as 'open' by default and can later be marked as done.

    Args:
        message (str): A short description of the ToDo (e.g. "Buy groceries").

    Returns:
        str: Confirmation message with the ToDo ID.
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
    Listing all current ToDos stored in the system. However, only respond with the
    ones required/requested by the user.

    If the user asks to view their tasks, this tool returns them.
    You can filter for only open (unfinished) ToDos using the `only_open` flag.

    Args:
        only_open (bool): Set to True if only unfinished ToDos should be shown.

    Returns:
        str: Formatted list of ToDos or a message if none are found.
    """
    todos = load_todos()
    filtered = [todo for todo in todos if not todo["done"]] if only_open else todos
    if not filtered:
        return "No ToDos found."
    
    return "\n".join(f"[{'x' if t['done'] else ' '}] ({t['id']}) {t['message']} – {t['created_at']}" for t in filtered)

# Tool: Mark ToDo as done
@mcp.tool()
def mark_done(todo_id: str) -> str:
    """
    Mark a specific ToDo as completed.

    Use this when the user finishes a task and wants to mark it as done.
    The done timestamp is automatically stored.

    Args:
        todo_id (str): The 8-character ID of the ToDo to mark as done.

    Returns:
        str: Confirmation message or error if the ID was not found.
    """
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
    """
    Permanently delete a ToDo by ID.

    Use this if the user wants to remove a task, regardless of its status.
    Useful for cleaning up completed or obsolete entries.

    Args:
        todo_id (str): The 8-character ID of the ToDo to delete.

    Returns:
        str: Message indicating success or failure.
    """
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
    Provide the AI with all ToDos and ask it to summarize them.

    Use this when the user wants a concise summary or overview.
    The summary should group, filter, or prioritize tasks if helpful.

    Returns:
        str: Natural-language prompt listing all current ToDos.
    """
    todos = load_todos()
    if not todos:
        return "There are no ToDos to summarize."
    
    text = "\n".join(f"{'[x]' if t['done'] else '[ ]'} {t['message']}" for t in todos)
    
    return f"Summarize the following ToDos:\n{text}"

# Resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """
    Return a personalized greeting in the context of ToDo management.

    Useful when the user first interacts with the system and may
    want to check their tasks or add new ones.

    Args:
        name (str): The user's name, used for personalization.

    Returns:
        str: A friendly greeting message.
    """
    return f"Hi {name}, would you like to manage your ToDos now?"

if __name__ == "__main__":
    print("ToDo system initialized at:", DATA_FILE)