# spreadsheet-agent

A side project I built to learn how to code AI agents.

It's a terminal chat agent that tracks my internship applications in a Google Sheet. You tell it what you applied for in plain English, and it can:

- **View** the applications already in the sheet
- **Add** new applications (Stage defaults to "Applied" and Date Applied to today)
- **Edit** existing applications, e.g. update the Stage or Date Replied
- **Email** you a summary whenever a new application is added

It uses Gemini (`gemini-3.6-flash`) through LangChain, the Google Sheets API, and Gmail.

## How to use it

1. **Set up Python 3.13 and install the packages:**

   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Set up Google Sheets access:**

   - Create a service account in Google Cloud, enable the Google Sheets API, and download its JSON key into this folder.
   - Share your Google Sheet with the service account's `client_email` (it's in the JSON key), the same way you'd share it with a person.
   - The sheet should have these columns in A to H: Company, Stage, Role, Location, Date Applied, Date Replied, Application Source, Details.
3. **Get a Gemini API key** from [Google AI Studio](https://aistudio.google.com/apikey).
4. **Create a Gmail App Password** at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords). You need 2-Step Verification turned on, and your normal Gmail password won't work.
5. **Create a `.env` file** in this folder:

   ```
   SPREADSHEET_ID=        # the long ID in your sheet's URL
   SHEET_NAME=            # the tab name, e.g. Internship_Applications
   SERVICE_ACCOUNT_FILE=  # path to the service account JSON key
   GOOGLE_API_KEY=        # your Gemini API key
   SENDER_EMAIL=          # Gmail address that sends the summary
   SENDER_PASSWORD=       # the Gmail App Password
   RECIPIENT_EMAIL=       # where the summary goes
   ```
6. **Run it:**

   ```bash
   python main.py
   ```

   Then try something like `I applied for a backend intern role at Shopee, found it on LinkedIn`. Type `exit` to quit.

## Files

| File              | What it does                                     |
| ----------------- | ------------------------------------------------ |
| `main.py`       | The agent: Gemini model, tools and the chat loop |
| `view_rows.py`  | Reads rows from the sheet                        |
| `edit_rows.py`  | Adds and edits rows in the sheet                 |
| `send_email.py` | Sends the summary email through Gmail            |

## Swapping the model

Feel free to swap out the model. To use a different Gemini model, change the name in `main.py`:

```python
model = ChatGoogleGenerativeAI(model="gemini-3.6-flash")
```

To use another provider, install its LangChain package (e.g. `langchain-openai` or `langchain-anthropic`), replace that line with the provider's chat model, and add its API key to `.env`. The tools and the rest of the agent stay the same.
