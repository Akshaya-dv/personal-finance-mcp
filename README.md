# Personal Finance Tracker MCP Server

## Project Overview

This project is a FastMCP-based Python server that allows AI assistants to log and analyse personal expenses using SQLite database storage.

The MCP server exposes tools that can:
- Log expenses
- Show spending summaries
- Check budget limits

---

## Tools Implemented

### 1. log_expense()
Stores expense information into SQLite database.

### 2. summarise_spending()
Shows category-wise spending summary.

### 3. budget_alert()
Checks whether spending exceeds a specified budget.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastMCP | MCP server framework |
| SQLite | Local database |
| uv | Python package management |
| python-dotenv | Environment variable management |

---

## Setup Instructions

### Clone Repository

```bash
git clone YOUR_REPO_URL
cd personal-finance-mcp
```

### Install Dependencies

```bash
uv sync
```

---

## Run the Server

```bash
uv run server.py
```

Server runs at:

```text
http://127.0.0.1:8000/mcp
```

---

## Example Prompts

```text
Log ₹450 for food — had lunch at cafe.
Show my spending summary.
Am I over budget on food if limit is ₹3000?
```
