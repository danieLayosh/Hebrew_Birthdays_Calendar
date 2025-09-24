#!/usr/bin/env python3
"""
Setup and installation script for Hebrew Birthdays Calendar.

This script helps users set up the environment and configure the application.
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def install_requirements():
    """Install Python requirements."""
    print("Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install requirements: {e}")
        return False


def create_config_file():
    """Create configuration file from template."""
    config_file = "config.json"
    template_file = "config_template.json"
    
    if os.path.exists(config_file):
        response = input(f"Config file '{config_file}' already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Keeping existing config file")
            return True
    
    try:
        if os.path.exists(template_file):
            # Copy template to config
            with open(template_file, 'r') as f:
                config_data = json.load(f)
            
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            print(f"✓ Created {config_file} from template")
        else:
            # Create basic config
            basic_config = {
                "google_calendar": {
                    "credentials_file": "credentials.json",
                    "token_file": "token.json"
                },
                "hebrew_birthdays": [],
                "settings": {
                    "years_ahead": 5,
                    "start_year": None,
                    "log_level": "INFO"
                }
            }
            
            with open(config_file, 'w') as f:
                json.dump(basic_config, f, indent=2)
            
            print(f"✓ Created basic {config_file}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to create config file: {e}")
        return False


def check_credentials():
    """Check if Google Calendar credentials are available."""
    credentials_file = "credentials.json"
    
    if os.path.exists(credentials_file):
        print(f"✓ Found Google Calendar credentials file: {credentials_file}")
        return True
    else:
        print(f"⚠ Google Calendar credentials file not found: {credentials_file}")
        print("\nTo get your credentials:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select an existing one")
        print("3. Enable the Google Calendar API")
        print("4. Create credentials (OAuth 2.0 Client ID)")
        print("5. Download the credentials JSON file")
        print(f"6. Save it as '{credentials_file}' in this directory")
        print("\nYou can run the script without credentials to test date conversion functionality.")
        return False


def run_test():
    """Run a basic test of the Hebrew date conversion."""
    print("\nTesting Hebrew date conversion...")
    try:
        from pyluach.dates import HebrewDate
        
        # Test conversion
        hebrew_date = HebrewDate(5784, 7, 15)  # 15th of Nisan, 5784
        gregorian_date = hebrew_date.to_greg()
        
        print(f"✓ Test conversion successful:")
        print(f"  Hebrew date: 15/7/5784 (15th of Nisan, 5784)")
        print(f"  Gregorian date: {gregorian_date.year}-{gregorian_date.month:02d}-{gregorian_date.day:02d}")
        return True
        
    except ImportError as e:
        print(f"✗ pyluach not imported properly: {e}")
        print("  Try: pip3 install --user pyluach")
        return False
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def main():
    """Main setup function."""
    print("Hebrew Birthdays Calendar Setup")
    print("=" * 35)
    
    # Check if we're in the right directory
    if not os.path.exists("hebrew_calendar.py"):
        print("✗ Error: hebrew_calendar.py not found. Please run this script from the project directory.")
        sys.exit(1)
    
    success = True
    
    # Install requirements
    success &= install_requirements()
    
    # Create config file
    success &= create_config_file()
    
    # Check credentials
    credentials_available = check_credentials()
    
    # Run test
    success &= run_test()
    
    print("\n" + "=" * 35)
    if success:
        print("✓ Setup completed successfully!")
        
        if credentials_available:
            print("\nYou can now run: python3 hebrew_calendar.py")
        else:
            print("\nNext steps:")
            print("1. Set up Google Calendar API credentials (see instructions above)")
            print("2. Edit config.json to add your Hebrew birthdays")
            print("3. Run: python3 hebrew_calendar.py")
    else:
        print("✗ Setup completed with some errors. Please check the messages above.")
    
    print("\nFor more information, see the README.md file.")


if __name__ == "__main__":
    main()