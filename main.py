"""Chat agent that manages the internship applications Google Sheet.

Gemini reads, adds and edits rows through the tools below, and emails a
summary after adding new applications. Run with: python main.py
"""

from datetime import date
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from view_rows import get_spreadsheet_data
from edit_rows import add_spreadsheet_data, edit_spreadsheet_data
from send_email import send_email

load_dotenv()

# Sheet columns A to H, in order
COLUMNS = ["Company", "Stage", "Role", "Location", "Date Applied", "Date Replied", "Application Source", "Details"]

@tool
def view_applications() -> list[dict]:
    """Get every row of the internship applications sheet with its sheet row number.
    Row 1 is the header."""
    rows = get_spreadsheet_data()
    return [{"row_number": i, "values": row} for i, row in enumerate(rows, start=1)]


@tool
def add_applications(rows: list[list[str]]) -> str:
    """Add one or more internship applications to the sheet.

    Each row must have exactly 8 values in this order:
    Company, Stage, Role, Location, Date Applied, Date Replied, Application Source, Details.
    Use "" for unknown values.
    """
    result = add_spreadsheet_data(rows)
    return f"Added {len(rows)} row(s) at {result['updatedRange']}"


@tool
def edit_application(row_number: int, new_row: list[str]) -> str:
    """Replace an existing application row in the sheet.

    row_number is the sheet row number from view_applications (2 or higher).
    new_row must have all 8 values in column order, so copy the unchanged
    values from the current row and change only what the user asked for.
    """
    if row_number < 2:
        return "Error: row 1 is the header and cannot be edited."
    result = edit_spreadsheet_data(row_number, new_row)
    return f"Updated {result['updatedRange']}"


@tool
def send_summary_email(subject: str, body: str) -> str:
    """Email a plain-text summary to the user's configured recipient address."""
    send_email(subject, body)
    return "Email sent"


# --- Agent ---

# Instructions Gemini follows for every message. Today's date is filled in at startup.
SYSTEM_PROMPT = f"""You manage the user's internship applications spreadsheet.

Columns: {", ".join(COLUMNS)}.
Today's date is {date.today().strftime("%d/%m/%Y")}. Write all dates as DD/MM/YYYY.
When adding a new application, use "Applied" for Stage and today's date for Date Applied
unless the user says otherwise.
Check the existing rows before adding, so you don't add duplicates.
After adding rows successfully, call send_summary_email once with a short summary
of every new entry (company, role, location, date applied and source).
To edit an application (e.g. a new Stage or a Date Replied), call view_applications
first to find its row number and current values, then call edit_application.
If more than one row matches, ask the user which one they mean."""

# Uses GOOGLE_API_KEY from .env
model = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

# The agent loops: Gemini calls tools, sees their results, and repeats until it can reply
agent = create_agent(
    model=model,
    tools=[view_applications, add_applications, edit_application, send_summary_email],
    system_prompt=SYSTEM_PROMPT,
)


def main():
    """Chat with the agent in the terminal until the user types 'exit'."""
    # Full conversation history, so the agent remembers earlier messages
    messages = []
    print("Spreadsheet agent ready. Type 'exit' to quit.")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        result = agent.invoke({"messages": messages})
        # Keep everything the agent did (tool calls and results included) for the next turn
        messages = result["messages"]
        print(f"\nAgent: {messages[-1].text}")


if __name__ == "__main__":
    main()
