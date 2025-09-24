#!/usr/bin/env python3
"""
Hebrew Birthdays Calendar Script

This script converts Hebrew dates to Gregorian dates and integrates with Google Calendar API
to manage Hebrew birthday events.

Dependencies:
- google-api-python-client
- google-auth-httplib2 
- google-auth-oauthlib
- pyluach
- python-dateutil
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

try:
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
except ImportError:
    print("Google API client libraries not installed. Run: pip install -r requirements.txt")
    exit(1)

try:
    from pyluach import dates, hebrewcal
    from pyluach.dates import HebrewDate, GregorianDate
except ImportError:
    print("pyluach not installed. Run: pip install -r requirements.txt")
    exit(1)


class HebrewBirthdayCalendar:
    """Main class for managing Hebrew birthday calendar integration with Google Calendar."""
    
    # Google Calendar API scope - modify if you need different permissions
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.json'):
        """
        Initialize the Hebrew Birthday Calendar manager.
        
        Args:
            credentials_file: Path to Google Calendar API credentials JSON file
            token_file: Path to store/load OAuth2 token
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('hebrew_calendar.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def authenticate_google_calendar(self) -> bool:
        """
        Authenticate with Google Calendar API.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        creds = None
        
        # Load existing token if available
        if os.path.exists(self.token_file):
            try:
                creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
            except Exception as e:
                self.logger.warning(f"Failed to load existing token: {e}")
        
        # If no valid credentials, initiate OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    self.logger.error(f"Failed to refresh token: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(self.credentials_file):
                    self.logger.error(f"Credentials file {self.credentials_file} not found. "
                                    "Please download it from Google Cloud Console.")
                    return False
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    self.logger.error(f"Authentication failed: {e}")
                    return False
            
            # Save credentials for next run
            try:
                with open(self.token_file, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                self.logger.warning(f"Failed to save token: {e}")
        
        try:
            self.service = build('calendar', 'v3', credentials=creds)
            self.logger.info("Successfully authenticated with Google Calendar API")
            return True
        except Exception as e:
            self.logger.error(f"Failed to build Calendar service: {e}")
            return False
    
    def hebrew_to_gregorian(self, hebrew_day: int, hebrew_month: int, hebrew_year: int) -> Optional[GregorianDate]:
        """
        Convert Hebrew date to Gregorian date.
        
        Args:
            hebrew_day: Hebrew day (1-30)
            hebrew_month: Hebrew month (1-12, or 1-13 in leap years)  
            hebrew_year: Hebrew year
            
        Returns:
            GregorianDate object or None if conversion fails
        """
        try:
            hebrew_date = HebrewDate(hebrew_year, hebrew_month, hebrew_day)
            gregorian_date = hebrew_date.to_greg()
            self.logger.info(f"Converted Hebrew date {hebrew_day}/{hebrew_month}/{hebrew_year} "
                           f"to Gregorian {gregorian_date}")
            return gregorian_date
        except Exception as e:
            self.logger.error(f"Failed to convert Hebrew date {hebrew_day}/{hebrew_month}/{hebrew_year}: {e}")
            return None
    
    def get_hebrew_birthday_gregorian_dates(self, hebrew_day: int, hebrew_month: int, 
                                          start_year: int, num_years: int = 5) -> List[GregorianDate]:
        """
        Get Gregorian dates for Hebrew birthday occurrences over multiple years.
        
        Args:
            hebrew_day: Hebrew birthday day
            hebrew_month: Hebrew birthday month
            start_year: Starting Gregorian year to calculate from
            num_years: Number of years to calculate (default: 5)
            
        Returns:
            List of GregorianDate objects for birthday occurrences
        """
        birthday_dates = []
        
        for year_offset in range(num_years):
            gregorian_year = start_year + year_offset
            
            # Convert current Gregorian year to approximate Hebrew year
            try:
                # Get Hebrew year for beginning of Gregorian year
                greg_start = GregorianDate(gregorian_year, 1, 1)
                hebrew_year_start = greg_start.to_heb().year
                
                # Check both Hebrew years that might occur in this Gregorian year
                for hebrew_year in [hebrew_year_start, hebrew_year_start + 1]:
                    gregorian_date = self.hebrew_to_gregorian(hebrew_day, hebrew_month, hebrew_year)
                    if gregorian_date and gregorian_date.year == gregorian_year:
                        birthday_dates.append(gregorian_date)
                        break
                        
            except Exception as e:
                self.logger.error(f"Error calculating birthday for year {gregorian_year}: {e}")
                continue
        
        return sorted(birthday_dates, key=lambda d: (d.year, d.month, d.day))
    
    def create_calendar_event(self, date: GregorianDate, title: str, description: str = "") -> Optional[str]:
        """
        Create a Google Calendar event.
        
        Args:
            date: GregorianDate for the event
            title: Event title
            description: Event description (optional)
            
        Returns:
            Event ID if successful, None otherwise
        """
        if not self.service:
            self.logger.error("Google Calendar service not initialized. Call authenticate_google_calendar() first.")
            return None
        
        try:
            # Create event object
            event = {
                'summary': title,
                'description': description,
                'start': {
                    'date': f"{date.year:04d}-{date.month:02d}-{date.day:02d}",
                    'timeZone': 'UTC',
                },
                'end': {
                    'date': f"{date.year:04d}-{date.month:02d}-{date.day:02d}",
                    'timeZone': 'UTC',
                },
                'reminders': {
                    'useDefault': True,
                },
            }
            
            # Insert event
            event_result = self.service.events().insert(calendarId='primary', body=event).execute()
            event_id = event_result.get('id')
            
            self.logger.info(f"Created calendar event '{title}' for {date} with ID: {event_id}")
            return event_id
            
        except Exception as e:
            self.logger.error(f"Failed to create calendar event: {e}")
            return None
    
    def add_hebrew_birthday_events(self, name: str, hebrew_day: int, hebrew_month: int, 
                                 start_year: int = None, num_years: int = 5) -> List[str]:
        """
        Add Hebrew birthday events to Google Calendar for multiple years.
        
        Args:
            name: Person's name for the birthday event
            hebrew_day: Hebrew birthday day
            hebrew_month: Hebrew birthday month  
            start_year: Starting Gregorian year (default: current year)
            num_years: Number of years to add events for (default: 5)
            
        Returns:
            List of created event IDs
        """
        if start_year is None:
            start_year = datetime.now().year
            
        # Get Gregorian dates for Hebrew birthday
        birthday_dates = self.get_hebrew_birthday_gregorian_dates(
            hebrew_day, hebrew_month, start_year, num_years)
        
        event_ids = []
        for date in birthday_dates:
            title = f"{name}'s Hebrew Birthday"
            description = f"Hebrew birthday: {hebrew_day}/{hebrew_month}\nGregorian date: {date}"
            
            event_id = self.create_calendar_event(date, title, description)
            if event_id:
                event_ids.append(event_id)
        
        self.logger.info(f"Added {len(event_ids)} birthday events for {name}")
        return event_ids


def load_config(config_file: str = 'config.json') -> Optional[Dict]:
    """
    Load configuration from JSON file.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Configuration dictionary or None if loading fails
    """
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Configuration file '{config_file}' not found.")
        print("Run 'python3 setup.py' to create one, or create it manually from config_template.json")
        return None
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in configuration file: {e}")
        return None
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None


def main():
    """Main function - can work with config file or as standalone example."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Hebrew Birthdays Calendar Manager')
    parser.add_argument('--config', default='config.json', 
                       help='Configuration file path (default: config.json)')
    parser.add_argument('--test-conversion', action='store_true',
                       help='Test Hebrew to Gregorian date conversion without Google Calendar API')
    parser.add_argument('--hebrew-day', type=int, help='Hebrew day for single birthday (1-30)')
    parser.add_argument('--hebrew-month', type=int, help='Hebrew month for single birthday (1-12)')
    parser.add_argument('--name', help='Name for single birthday event')
    parser.add_argument('--years', type=int, default=5, help='Number of years ahead (default: 5)')
    
    args = parser.parse_args()
    
    # If testing conversion only
    if args.test_conversion:
        print("Testing Hebrew to Gregorian date conversion...")
        
        # Test with some example dates
        test_dates = [
            (15, 7, 5784),  # 15 Nisan 5784
            (1, 1, 5785),   # 1 Tishrei 5785 (Rosh Hashanah)
            (10, 1, 5785),  # 10 Tishrei 5785 (Yom Kippur)
        ]
        
        calendar = HebrewBirthdayCalendar()
        for hebrew_day, hebrew_month, hebrew_year in test_dates:
            gregorian_date = calendar.hebrew_to_gregorian(hebrew_day, hebrew_month, hebrew_year)
            if gregorian_date:
                print(f"Hebrew {hebrew_day}/{hebrew_month}/{hebrew_year} = Gregorian {gregorian_date.year}-{gregorian_date.month:02d}-{gregorian_date.day:02d}")
        
        return
    
    # Initialize the calendar manager
    calendar = HebrewBirthdayCalendar()
    
    # Handle single birthday from command line arguments
    if args.hebrew_day and args.hebrew_month and args.name:
        print(f"Processing single birthday for {args.name}")
        
        # Test conversion first
        current_year = datetime.now().year
        birthday_dates = calendar.get_hebrew_birthday_gregorian_dates(
            args.hebrew_day, args.hebrew_month, current_year, args.years)
        
        if not birthday_dates:
            print("No valid birthday dates found for the specified Hebrew date.")
            return
            
        print(f"Found {len(birthday_dates)} birthday dates:")
        for date in birthday_dates:
            print(f"  {date.year}-{date.month:02d}-{date.day:02d}")
        
        # Authenticate and create events
        if calendar.authenticate_google_calendar():
            event_ids = calendar.add_hebrew_birthday_events(
                name=args.name,
                hebrew_day=args.hebrew_day,
                hebrew_month=args.hebrew_month,
                num_years=args.years
            )
            
            if event_ids:
                print(f"✓ Successfully created {len(event_ids)} birthday events!")
            else:
                print("✗ No events were created.")
        else:
            print("✗ Failed to authenticate with Google Calendar.")
        
        return
    
    # Load configuration file
    config = load_config(args.config)
    if not config:
        # Fallback to example usage
        print("Using example configuration since no config file found...")
        
        calendar = HebrewBirthdayCalendar()
        
        # Test conversion without Google Calendar
        example_dates = [
            ("Example Person", 15, 7),  # 15 Nisan
        ]
        
        print("Testing Hebrew date conversions:")
        current_year = datetime.now().year
        for name, hebrew_day, hebrew_month in example_dates:
            birthday_dates = calendar.get_hebrew_birthday_gregorian_dates(
                hebrew_day, hebrew_month, current_year, 3)
            print(f"\n{name} (Hebrew: {hebrew_day}/{hebrew_month}):")
            for date in birthday_dates:
                print(f"  {date.year}-{date.month:02d}-{date.day:02d}")
        
        print("\nTo add events to Google Calendar:")
        print("1. Run 'python3 setup.py' to set up credentials and config")
        print("2. Or use command line: python3 hebrew_calendar.py --name 'John' --hebrew-day 15 --hebrew-month 7")
        return
    
    # Use configuration
    google_config = config.get('google_calendar', {})
    birthdays = config.get('hebrew_birthdays', [])
    settings = config.get('settings', {})
    
    if not birthdays:
        print("No birthdays configured. Please edit your config file to add Hebrew birthdays.")
        return
    
    # Initialize with custom credentials paths
    calendar = HebrewBirthdayCalendar(
        credentials_file=google_config.get('credentials_file', 'credentials.json'),
        token_file=google_config.get('token_file', 'token.json')
    )
    
    # Authenticate with Google Calendar
    if not calendar.authenticate_google_calendar():
        print("Failed to authenticate with Google Calendar. Events will not be created.")
        
        # Still show conversion results
        print("\nHebrew to Gregorian date conversions:")
        current_year = settings.get('start_year') or datetime.now().year
        years_ahead = settings.get('years_ahead', 5)
        
        for birthday in birthdays:
            name = birthday.get('name', 'Unknown')
            hebrew_day = birthday.get('hebrew_day')
            hebrew_month = birthday.get('hebrew_month')
            
            if hebrew_day and hebrew_month:
                birthday_dates = calendar.get_hebrew_birthday_gregorian_dates(
                    hebrew_day, hebrew_month, current_year, years_ahead)
                print(f"\n{name} (Hebrew: {hebrew_day}/{hebrew_month}):")
                for date in birthday_dates:
                    print(f"  {date.year}-{date.month:02d}-{date.day:02d}")
        
        return
    
    # Process all birthdays from config
    current_year = settings.get('start_year') or datetime.now().year
    years_ahead = settings.get('years_ahead', 5)
    total_events = 0
    
    print(f"Processing {len(birthdays)} birthdays for {years_ahead} years starting from {current_year}...")
    
    for birthday in birthdays:
        name = birthday.get('name', 'Unknown')
        hebrew_day = birthday.get('hebrew_day')
        hebrew_month = birthday.get('hebrew_month')
        
        if not hebrew_day or not hebrew_month:
            print(f"⚠ Skipping {name}: missing Hebrew day or month")
            continue
        
        print(f"\nProcessing {name} (Hebrew: {hebrew_day}/{hebrew_month})...")
        
        event_ids = calendar.add_hebrew_birthday_events(
            name=name,
            hebrew_day=hebrew_day,
            hebrew_month=hebrew_month,
            start_year=current_year,  
            num_years=years_ahead
        )
        
        if event_ids:
            print(f"  ✓ Created {len(event_ids)} events")
            total_events += len(event_ids)
        else:
            print(f"  ✗ No events created")
    
    print(f"\n🎉 Total events created: {total_events}")


if __name__ == "__main__":
    main()