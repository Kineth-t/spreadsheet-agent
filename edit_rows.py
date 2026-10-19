import os
from datetime import date
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")

def add_spreadsheet_data(rows):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    # append() treats the table's empty rows as used and writes below the table,
    # so find the first empty row ourselves. get() drops trailing empty rows.
    existing_rows = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{SHEET_NAME}'!A:H",
        )
        .execute()
        .get('values', [])
    )
    first_row = len(existing_rows) + 1
    last_row = first_row + len(rows) - 1

    body = {
        'values': rows
    }

    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{SHEET_NAME}'!A{first_row}:H{last_row}",
            valueInputOption='USER_ENTERED',
            body=body
        )
        .execute()
    )

    return result

today = date.today().strftime("%d/%m/%Y")

fake_rows = [
    # Company, Stage, Role, Location, Date Applied, Date Replied, Application Source, Details
    ["Office of the President", "Applied", "Intern President (Part-time, Weekends Only)", "The Oval Office", today, "", "https://www.linkedin.com/jobs/president", ""],
    ["Hogwarts", "Applied", "Defence Against the Dark Arts Intern", "Scotland", today, "", "https://www.hogwarts.edu/careers", ""],
    ["NASA", "Applied", "Moon Cheese Quality Inspector", "The Moon", today, "", "https://www.nasa.gov/careers", ""],
]

print(add_spreadsheet_data(fake_rows))