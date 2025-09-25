from services.dateConvertionLogic import parse_hebrew_date
import csv

def normalize_hebrew_text(text):
    # strip spaces/quotes and unify apostrophes
    text = text.strip()
    text = text.replace('"', '')         # remove double quotes
    text = text.replace("'", "’")       # convert straight to curly apostrophe
    text = text.replace("`", "’")       # optional: handle backticks
    return text


def read_birthdays_from_csv(file_path):
    birthdays = []
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Clean the values
            day_text = row['יום'].strip().replace('"', '')
            month_text = normalize_hebrew_text(row['חודש'])
            year_text = row['שנה'].strip().replace('"', '')
            name_text = row['שם'].strip().replace('"', '')

            year, month, day = parse_hebrew_date(
                day_text=day_text,
                month_text=month_text,
                year_text=year_text
            )
            birthdays.append((year, month, day, name_text))
    return birthdays
