import os
from dotenv import load_dotenv
from services.googleCalendarAPI import genrate_service_client, create_calendar, add_full_day_event
from services.dateConvertionLogic import convert_hebrew_to_gregorian, convert_heb_year_to_gregorian

# Load variables from .env
load_dotenv()

CREDENTIALS_PATH = os.getenv("CREDENTIALS_PATH")

def main():
    print("Starting the script...")
    # Add your main logic here
    
    service = genrate_service_client(credentials_path=CREDENTIALS_PATH)
    calendar_id = create_calendar(service)
    
    birthday_list = [
        (5765, 12, 29, "Daniel Layosh")
    ]
    
    for hebrew_year, hebrew_month, hebrew_day, name in birthday_list:
        for i in range(0, 100):
            # Convert Hebrew date to Gregorian date
            gregorian_date = convert_hebrew_to_gregorian((hebrew_year + i, hebrew_month, hebrew_day))
            gregorian_year, gregorian_month, gregorian_day = gregorian_date

            # Format date as 'YYYY-MM-DD'
            event_date = f"{gregorian_year:04d}-{gregorian_month:02d}-{gregorian_day:02d}"

            age = gregorian_year - convert_heb_year_to_gregorian(heb_year=hebrew_year, heb_month=hebrew_month, heb_day=hebrew_day)

            # Add full-day event to the calendar
            add_full_day_event(
                service,
                calendar_id,
                summary=f"{name}'s Birthday",
                event_date=event_date,
                description=f"{age} Birthday of {name}",
            )


if __name__ == "__main__":
    main()