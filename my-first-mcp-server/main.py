from mcp.server.fastmcp import FastMCP
from typing import List

# In-memory mock database with 10 rows
employee_leaves = {
    "E001": {"balance": 18, "history": ["2024-12-25", "2025-01-01"]},
    "E002": {"balance": 20, "history": []},
    "E003": {"balance": 5, "history": ["2025-02-10", "2025-02-11", "2025-02-12"]},
    "E004": {"balance": 12, "history": ["2024-11-20"]},
    "E005": {"balance": 25, "history": []},
    "E006": {"balance": 15, "history": ["2025-03-01", "2025-03-02"]},
    "E007": {"balance": 8, "history": ["2025-01-15"]},
    "E008": {"balance": 22, "history": []},
    "E009": {"balance": 10, "history": ["2024-12-30"]},
    "E010": {"balance": 30, "history": []}
}

# Create MCP server
mcp = FastMCP("LeaveManager")

# Tool: Check Leave Balance
@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """Check how many leave days are left for the employee"""
    data = employee_leaves.get(employee_id)
    if data:
        return f"{employee_id} has {data['balance']} leave days remaining."
    return f"Employee ID {employee_id} not found."

# Tool: Apply for Leave
@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    """Apply leave for specific dates (e.g., ["2025-04-17", "2025-05-01"])"""
    if employee_id not in employee_leaves:
        return f"Employee ID {employee_id} not found."

    requested_days = len(leave_dates)
    available_balance = employee_leaves[employee_id]["balance"]

    if available_balance < requested_days:
        return f"Insufficient balance. Requested {requested_days}, available {available_balance}."

    # Deduct balance and add to history
    employee_leaves[employee_id]["balance"] -= requested_days
    employee_leaves[employee_id]["history"].extend(leave_dates)
    return f"Leave applied successfully for {requested_days} day(s). New balance for {employee_id}: {employee_leaves[employee_id]['balance']}."

# Tool: Get Leave History
@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    """Get the list of dates the employee was previously on leave"""
    data = employee_leaves.get(employee_id)
    if data:
        history = ", ".join(data['history']) if data['history'] else "No previous leaves recorded."
        return f"Leave history for {employee_id}: {history}"
    return f"Employee ID {employee_id} not found."

# Resource: Greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! I am your HR Leave Management Assistant. How can I help you today?"

if __name__ == "__main__":
    mcp.run()