"""Read rows from the internship applications Google Sheet."""

import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

load_dotenv()

# Settings from .env
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")  # path to the service account JSON key
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")              # the long ID in the sheet's URL
SHEET_NAME = os.getenv("SHEET_NAME")                      # the tab name, e.g. Internship_Applications

def get_spreadsheet_data():
    """Return every row in columns A to H as a list of lists, header row included.

    Empty cells at the end of a row are left out, so some rows can be shorter than 8.
    """
    # Log in as the service account and create a Sheets API client
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    # Quotes around the sheet name keep names with spaces working
    all_rows = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{SHEET_NAME}'!A:H",
        )
        .execute()['values']
    )

    return all_rows
