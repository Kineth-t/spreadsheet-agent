"""Add and edit rows in the internship applications Google Sheet."""

import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

load_dotenv()

# Settings from .env
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")  # path to the service account JSON key
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")              # the long ID in the sheet's URL
SHEET_NAME = os.getenv("SHEET_NAME")                      # the tab name, e.g. Internship_Applications

def add_spreadsheet_data(rows):
    """Write one or more rows starting at the first empty row of the sheet.

    rows is a list of rows, and each row is a list of 8 values (columns A to H).
    Returns the Sheets API response, which includes the 'updatedRange' written.
    """
    # Log in as the service account and create a Sheets API client
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

    # USER_ENTERED makes Sheets treat values as if typed in, so dates become real dates
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
    """Overwrite one whole row (columns A to H) with new_row.

    row_number is the sheet's row number (row 1 is the header).
    new_row is a list of 8 values, so unchanged values must be passed in too.
    """
    # Log in as the service account and create a Sheets API client
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
