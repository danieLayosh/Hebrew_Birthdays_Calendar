#!/usr/bin/env python3
"""
Quick example runner for Hebrew Birthdays Calendar

This script demonstrates the Hebrew date conversion functionality without requiring
Google Calendar API credentials.
"""

from hebrew_calendar import HebrewBirthdayCalendar
from datetime import datetime

def main():
    print("Hebrew Birthdays Calendar - Example Usage")
    print("=" * 45)
    
    # Initialize the calendar (without Google Calendar for this example)
    calendar = HebrewBirthdayCalendar()
    
    # Example Hebrew birthdays to convert
    example_birthdays = [
        ("David Cohen", 15, 7),      # 15th of Nisan
        ("Sarah Levi", 1, 1),        # 1st of Tishrei (Rosh Hashanah)
        ("Michael Ben-David", 10, 1), # 10th of Tishrei (Yom Kippur)
        ("Rachel Goldberg", 25, 3),   # 25th of Kislev (Hanukkah)
        ("Jonathan Rosen", 15, 5),    # 15th of Shvat (Tu BiShvat)
    ]
    
    current_year = datetime.now().year
    years_to_show = 3
    
    print(f"\nConverting Hebrew birthdays to Gregorian dates:")
    print(f"Showing next {years_to_show} years starting from {current_year}")
    print("-" * 60)
    
    for name, hebrew_day, hebrew_month in example_birthdays:
        print(f"\n{name} - Hebrew Birthday: {hebrew_day}/{hebrew_month}")
        
        # Get Hebrew month name for display
        month_names = [
            "Tishrei", "Cheshvan", "Kislev", "Tevet", "Shvat", "Adar",
            "Nisan", "Iyar", "Sivan", "Tammuz", "Av", "Elul"
        ]
        month_name = month_names[hebrew_month - 1] if 1 <= hebrew_month <= 12 else f"Month {hebrew_month}"
        print(f"  ({hebrew_day} {month_name})")
        
        # Get Gregorian dates for this birthday
        birthday_dates = calendar.get_hebrew_birthday_gregorian_dates(
            hebrew_day, hebrew_month, current_year, years_to_show
        )
        
        if birthday_dates:
            print("  Gregorian dates:")
            for date in birthday_dates:
                print(f"    {date.year}-{date.month:02d}-{date.day:02d} ({date.strftime('%A, %B %d, %Y')})")
        else:
            print("    No valid dates found")
    
    print("\n" + "=" * 45)
    print("To add these events to Google Calendar:")
    print("1. Run: python3 setup.py")
    print("2. Set up Google Calendar API credentials")
    print("3. Edit config.json with your birthdays")
    print("4. Run: python3 hebrew_calendar.py")
    print("\nOr use command line for a single birthday:")
    print("python3 hebrew_calendar.py --name 'John Doe' --hebrew-day 15 --hebrew-month 7")

if __name__ == "__main__":
    main()