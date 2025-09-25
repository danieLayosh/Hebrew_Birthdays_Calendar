import os
from dotenv import load_dotenv
from services.googleCalendarAPI import (
    genrate_service_client,
    create_calendar,
    add_full_day_event,
    share_calendar_with_user,
)
from services.dateConvertionLogic import convert_hebrew_to_gregorian, convert_heb_year_to_gregorian
from services.csv_functions import read_birthdays_from_csv

import time

load_dotenv()

CREDENTIALS_PATH = os.getenv("CREDENTIALS_PATH")
BIRTHDAY_CSV_PATH = os.getenv("BIRTHDAY_CSV_PATH")
SHARE_EMAIL = os.getenv("SHARE_EMAIL")  # the target account
MY_EMAIL = os.getenv("MY_EMAIL")        # your account

def main():
    print("Starting the script...")

    service = genrate_service_client(credentials_path=CREDENTIALS_PATH)
    calendar_id = create_calendar(service)

    birthday_list = read_birthdays_from_csv(BIRTHDAY_CSV_PATH)

    # Add all birthday events
    for hebrew_year, hebrew_month, hebrew_day, name in birthday_list:
        for i in range(0, 100):
            gregorian_date = convert_hebrew_to_gregorian((hebrew_year + i, hebrew_month, hebrew_day))
            gregorian_year, gregorian_month, gregorian_day = gregorian_date

            event_date = f"{gregorian_year:04d}-{gregorian_month:02d}-{gregorian_day:02d}"
            age = gregorian_year - convert_heb_year_to_gregorian(
                heb_year=hebrew_year, heb_month=hebrew_month, heb_day=hebrew_day
            )

            add_full_day_event(
                service,
                calendar_id,
                summary=f"{name}'s Birthday",
                event_date=event_date,
                description=f"{age} Birthday of {name}",
            )
            time.sleep(0.1)

    # Share calendar with target account (writer role)
    share_calendar_with_user(service, calendar_id, SHARE_EMAIL, role="writer")
    print(f"Calendar shared with {SHARE_EMAIL}. Ask them to accept and make themselves owner in Google Calendar UI.")

if __name__ == "__main__":
    main()
