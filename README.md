# Hebrew Birthdays Calendar

A Python script that converts Hebrew dates to Gregorian dates and automatically creates birthday events in Google Calendar. This tool helps you keep track of Hebrew birthdays by automatically calculating when they occur each year in the Gregorian calendar and creating corresponding calendar events.

## Features

- **Hebrew to Gregorian Date Conversion**: Uses the `pyluach` library for accurate Hebrew calendar conversions
- **Google Calendar Integration**: Automatically creates birthday events in your Google Calendar
- **Multi-Year Support**: Creates events for multiple years ahead (configurable)
- **Configuration File Support**: Manage multiple birthdays through a JSON configuration file
- **Command Line Interface**: Support for both batch processing and single birthday entries
- **Flexible Authentication**: OAuth2 authentication with token persistence
- **Comprehensive Logging**: Detailed logging for troubleshooting and monitoring

## Prerequisites

- Python 3.7 or higher
- Google Calendar API credentials
- Required Python packages (see requirements.txt)

## Installation

### Quick Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/danieLayosh/Hebrew_Birthdays_Calendar.git
   cd Hebrew_Birthdays_Calendar
   ```

2. Run the setup script:
   ```bash
   python3 setup.py
   ```

   This will:
   - Install required Python packages
   - Create a configuration file template
   - Test the Hebrew date conversion functionality
   - Provide instructions for Google Calendar API setup

### Manual Setup

1. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

2. Set up Google Calendar API credentials:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Calendar API
   - Create OAuth 2.0 credentials
   - Download the credentials JSON file and save it as `credentials.json`

3. Create configuration file:
   ```bash
   cp config_template.json config.json
   ```

## Configuration

Edit `config.json` to add your Hebrew birthdays:

```json
{
  "google_calendar": {
    "credentials_file": "credentials.json",
    "token_file": "token.json"
  },
  "hebrew_birthdays": [
    {
      "name": "John Doe",
      "hebrew_day": 15,
      "hebrew_month": 7,
      "notes": "15th of Nisan"
    },
    {
      "name": "Jane Smith",
      "hebrew_day": 5,
      "hebrew_month": 1,
      "notes": "5th of Tishrei"
    }
  ],
  "settings": {
    "years_ahead": 5,
    "start_year": null,
    "log_level": "INFO"
  }
}
```

### Hebrew Month Numbers

The Hebrew months are numbered as follows:
- 1 = Tishrei (רגש)
- 2 = Cheshvan (ןושח)
- 3 = Kislev (ולסכ)
- 4 = Tevet (תבט)
- 5 = Shvat (טבש)
- 6 = Adar (רדא)
- 7 = Nisan (ןסינ)
- 8 = Iyar (רייא)
- 9 = Sivan (ןויס)
- 10 = Tammuz (זומת)
- 11 = Av (בא)
- 12 = Elul (לולא)

In leap years, there's also:
- 13 = Adar II (רדא ב)

## Usage

### Using Configuration File

Process all birthdays from your configuration file:
```bash
python3 hebrew_calendar.py
```

### Command Line Arguments

Add a single birthday:
```bash
python3 hebrew_calendar.py --name "John Doe" --hebrew-day 15 --hebrew-month 7 --years 5
```

Test date conversion without Google Calendar:
```bash
python3 hebrew_calendar.py --test-conversion
```

Use custom configuration file:
```bash
python3 hebrew_calendar.py --config my_config.json
```

### Command Line Options

- `--config`: Path to configuration file (default: config.json)
- `--test-conversion`: Test Hebrew to Gregorian conversion without Google Calendar API
- `--hebrew-day`: Hebrew day for single birthday (1-30)
- `--hebrew-month`: Hebrew month for single birthday (1-12)
- `--name`: Name for single birthday event
- `--years`: Number of years ahead (default: 5)

## How It Works

1. **Date Conversion**: The script uses the `pyluach` library to convert Hebrew dates to Gregorian dates. Since Hebrew years don't align perfectly with Gregorian years, the script calculates the appropriate Hebrew year for each Gregorian year.

2. **Google Calendar Integration**: Uses the Google Calendar API to create all-day events for each birthday occurrence.

3. **Multi-Year Processing**: For each Hebrew birthday, the script calculates when it occurs in each requested Gregorian year and creates calendar events accordingly.

## Examples

### Example 1: Single Birthday
```bash
# Add events for someone born on 15th of Nisan for the next 3 years
python3 hebrew_calendar.py --name "Sarah Cohen" --hebrew-day 15 --hebrew-month 7 --years 3
```

### Example 2: Test Conversion
```bash
# Test Hebrew date conversion without creating calendar events
python3 hebrew_calendar.py --test-conversion
```

### Example 3: Batch Processing
Edit your `config.json` file and run:
```bash
python3 hebrew_calendar.py
```

## Troubleshooting

### Common Issues

1. **"Credentials not found" error**:
   - Make sure you've downloaded the Google Calendar API credentials
   - Save the file as `credentials.json` in the project directory

2. **Authentication fails**:
   - Delete `token.json` and re-authenticate
   - Check that your Google Cloud project has the Calendar API enabled

3. **Date conversion errors**:
   - Verify Hebrew month numbers (1-12, or 1-13 in leap years)
   - Check that Hebrew day is valid for the given month

4. **No events created**:
   - Check the log file `hebrew_calendar.log` for detailed error messages
   - Verify your Google Calendar permissions

### Log Files

The script creates a log file `hebrew_calendar.log` with detailed information about operations, errors, and conversions. Check this file for troubleshooting.

## Dependencies

- `google-api-python-client`: Google Calendar API client
- `google-auth-httplib2`: Google authentication HTTP library
- `google-auth-oauthlib`: OAuth2 authentication flow
- `pyluach`: Hebrew calendar conversion library
- `python-dateutil`: Date utilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source. Please check the repository for license details.

## Hebrew Calendar Information

This script uses the `pyluach` library, which provides accurate Hebrew calendar calculations including:
- Regular and leap years
- Varying month lengths
- Accurate conversion between Hebrew and Gregorian dates

The Hebrew calendar is a lunisolar calendar, meaning Hebrew birthdays don't occur on the same Gregorian date each year. This script automatically handles these variations.