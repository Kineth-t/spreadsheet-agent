from datetime import date
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from view_rows import get_spreadsheet_data
from edit_rows import add_spreadsheet_data
from send_email import send_email

load_dotenv()

COLUMNS = ["Company", "Stage", "Role", "Location", "Date Applied", "Date Replied", "Application Source", "Details"]


@tool
def view_applications() -> list[list[str]]:
    """Get every row of the internship applications sheet. The first row is the header."""
    return get_spreadsheet_data()


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
def send_summary_email(subject: str, body: str) -> str:
    """Email a plain-text summary to the user's configured recipient address."""
    send_email(subject, body)
    return "Email sent"


SYSTEM_PROMPT = f"""You manage the user's internship applications spreadsheet.

Columns: {", ".join(COLUMNS)}.
Today's date is {date.today().strftime("%d/%m/%Y")}. Write all dates as DD/MM/YYYY.
When adding a new application, use "Applied" for Stage and today's date for Date Applied
unless the user says otherwise.
Check the existing rows before adding, so you don't add duplicates.
After adding rows successfully, call send_summary_email once with a short summary
of every new entry (company, role, location, date applied and source)."""

model = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

agent = create_agent(
    model=model,
    tools=[view_applications, add_applications, send_summary_email],
    system_prompt=SYSTEM_PROMPT,
)


def main():
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
        messages = result["messages"]
        print(f"\nAgent: {messages[-1].text}")


if __name__ == "__main__":
    main()
