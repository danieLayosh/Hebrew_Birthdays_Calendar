from dateConvertionLogic import hebrew_gematria_to_num, hebrew_year_to_num, parse_hebrew_date
import csv

def read_birthdays_from_csv(file_path):
    birthdays = []
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            year, month, day = parse_hebrew_date(
                day_text=row['יום'],
                month_text=row['חודש'],
                year_text=row['שנה']
            )
            birthdays.append((year, month, day, row['שם']))
    return birthdays


lista = read_birthdays_from_csv('src/services/birthdays.csv') 