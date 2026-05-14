import os
import sqlite3
from datetime import datetime

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

# Read HOST and PORT from .env file
_host = os.environ.get("HOST", "127.0.0.1")
_port = int(os.environ.get("PORT", "8000"))

# Create MCP server
mcp = FastMCP(
    "personal-finance-mcp",
    host=_host,
    port=_port,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False
    ),
)

# Database file name
DB_NAME = "expenses.db"


# Create database table if not exists
def init_db():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            note TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# Tool 1 - Log Expense
@mcp.tool()
def log_expense(amount: float, category: str, note: str = "") -> str:
    """
    Save an expense into SQLite database.
    """

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (amount, category, note, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        amount,
        category,
        note,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return f"Expense of ₹{amount} added under '{category}'."


# Tool 2 - Summarise Spending
@mcp.tool()
def summarise_spending(period: str = "this month") -> str:
    """
    Show spending summary grouped by category.
    """

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    results = cursor.fetchall()

    conn.close()

    if not results:
        return "No expenses found."

    summary = "Spending Summary:\n"

    for category, total in results:
        summary += f"- {category}: ₹{total}\n"

    return summary


# Tool 3 - Budget Alert
@mcp.tool()
def budget_alert(category: str, limit: float) -> str:
    """
    Check whether spending crossed budget limit.
    """

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE category = ?
    """, (category,))

    result = cursor.fetchone()

    conn.close()

    total = result[0] if result[0] else 0

    if total > limit:
        return (
            f"Budget exceeded for {category}. "
            f"Spent ₹{total} out of ₹{limit}."
        )

    return (
        f"Budget is under control for {category}. "
        f"Spent ₹{total} out of ₹{limit}."
    )


def main():
    init_db()

    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()