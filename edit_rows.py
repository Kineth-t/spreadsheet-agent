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

def edit_spreadsheet_data(row_number, new_row):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    body = {
        'values': [new_row]
    }

    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{SHEET_NAME}'!A{row_number}:H{row_number}",
            valueInputOption='USER_ENTERED',
            body=body
        )
        .execute()
    )

    return result

if __name__ == "__main__":
    today = date.today().strftime("%d/%m/%Y")