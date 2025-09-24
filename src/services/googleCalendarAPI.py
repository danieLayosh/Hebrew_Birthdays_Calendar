import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def genrate_service_client(credentials_path="../../credentials.json"):

  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          credentials_path, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)
    return service

  except HttpError as error:
    print(f"An error occurred: {error}")


def create_calendar(service, calendar_name="Hebrew Birthdays Calendar", timezone="Asia/Jerusalem"):
    # Step 1: List all existing calendars
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for cal in calendar_list.get("items", []):
            if cal.get("summary") == calendar_name:
                print(f"Calendar already exists: {cal['id']}")
                return cal["id"]  # Return existing calendar ID
        page_token = calendar_list.get("nextPageToken")
        if not page_token:
            break

    # Step 2: Create a new calendar if it doesn't exist
    calendar = {
        "summary": calendar_name,
        "timeZone": timezone
    }
    created_calendar = service.calendars().insert(body=calendar).execute()
    print(f"Created calendar with ID: {created_calendar['id']}")
    return created_calendar["id"]



def add_full_day_event(service, calendar_id, summary, event_date, description="", location=""):
    """
    event_date should be a string in 'YYYY-MM-DD' format
    """
    event = {
        "summary": summary,
        "description": description,
        "location": location,
        "start": {"date": event_date},
        "end": {"date": event_date},
    }

    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")
    
    