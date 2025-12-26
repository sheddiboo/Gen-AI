# Leave Management MCP Server

An implementation of the **Model Context Protocol (MCP)** that provides an AI-driven interface for HR leave management. This server allows AI agents (like Claude Desktop) to interact with a mock employee leave database.

## General Overview

This project serves as a bridge between an AI Model (the "brain") and a local data source (the "memory"). Instead of manually searching through records, an HR administrator can use natural language to manage employee leave.

### How it Works
1. **The Server:** A Python script (`main.py`) using the FastMCP SDK defines specific tools: `get_leave_balance`, `apply_leave`, and `get_leave_history`.
2. **The Client:** Claude Desktop connects to this server via the `claude_desktop_config.json` file.
3. **The Interaction:** When a user asks about leave, the AI identifies the correct tool, executes the Python logic locally, and returns a natural language response.



## Core Features

* **Real-time Queries:** Check leave balances for 10+ pre-configured employee records.
* **Automated Updates:** Apply for specific leave dates; the server automatically calculates the duration and updates the remaining balance.
* **History Tracking:** Retrieve a list of all previously taken leave dates for any employee.
* **Secure Local Execution:** All data processing happens on your local machine, ensuring sensitive employee data is not shared globally.

## Project Structure

* `main.py`: Contains the mock database and MCP tool definitions.
* `pyproject.toml`: Manages project metadata and library dependencies via `uv`.
* `README.md`: Project documentation and overview.

---
*Developed as a technical showcase for automated HR operations using the Model Context Protocol.*