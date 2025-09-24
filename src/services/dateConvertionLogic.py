from pyluach import dates

# Mapping Hebrew month names to pyluach month numbers
HEBREW_MONTHS = {
    "תשרי": 7,
    "חשון": 8, "מרחשון": 8,
    "כסלו": 9,
    "טבת": 10,
    "שבט": 11,
    "אדר": 12,       # In non-leap years
    "אדר א": 12, "אדר א'": 12, "אדר ראשון": 12,
    "אדר ב": 13, "אדר ב'": 13, "אדר שני": 13,
    "ניסן": 1,
    "אייר": 2,
    "סיון": 3, "סיוון": 3,
    "תמוז": 4,
    "אב": 5,
    "אלול": 6,
}

# Hebrew gematria values for numbers
HEBREW_NUMS = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5,
    'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
    'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40,
    'נ': 50, 'ן': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80,
    'צ': 90, 'ץ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400
}

def convert_hebrew_to_gregorian(hebrew_date: tuple) -> tuple:
    """
    Convert a Hebrew date to a Gregorian date.
    First month is 1 (Nisan), last month is 12 or 13 (Adar II in leap years).

    Args:
        hebrew_date (tuple): A tuple containing the Hebrew date in the format (year, month, day).

    Returns:
        tuple: A tuple containing the corresponding Gregorian date in the format (year, month, day).
    """
    
    hebrew_year, hebrew_month, hebrew_day = hebrew_date
    hebrew_date_obj = dates.HebrewDate(hebrew_year, hebrew_month, hebrew_day)
    gregorian_date_obj = hebrew_date_obj.to_greg()
    return (gregorian_date_obj.year, gregorian_date_obj.month, gregorian_date_obj.day)
    

def convert_heb_year_to_gregorian(heb_year: int, heb_month: int, heb_day: int) -> int:
    """
    Convert a Hebrew year to the corresponding Gregorian year.
    The function assumes the Hebrew year starts in the fall of the Gregorian year.

    Args:
        heb_year (int): The Hebrew year to convert.
    Returns:
        int: The corresponding Gregorian year.  
    """
    # The Hebrew year starts in the fall of the Gregorian year
    # So, we convert the 1st of Tishrei (7th month) of the Hebrew year to Gregorian
    hebrew_date_obj = dates.HebrewDate(year=heb_year, month=heb_month, day=heb_day)  # 1st of Tishrei
    gregorian_date_obj = hebrew_date_obj.to_greg()
    return gregorian_date_obj.year


def hebrew_gematria_to_num(text: str) -> int:
    """Convert Hebrew letters (gematria) like י״ג or כ"ט to a number."""
    total = 0
    for ch in text:
        if ch in HEBREW_NUMS:
            total += HEBREW_NUMS[ch]
    return total

def hebrew_year_to_num(year_text: str) -> int:
    """Convert Hebrew year text like תשס"ה or שנת התשפ"ו to integer year (e.g. 5765, 5786)."""
    # Remove common prefixes
    year_text = year_text.replace("שנת", "").strip()
    
    # If it starts with 'ה' and the rest is a valid year (e.g. 'התשפ"ו'),
    # strip the leading 'ה'
    if year_text.startswith("ה") and len(year_text) > 1:
        year_text = year_text[1:]
    
    # Keep only Hebrew letters
    letters = ''.join(ch for ch in year_text if ch in HEBREW_NUMS)
    val = hebrew_gematria_to_num(letters)

    # Hebrew years are written without the 5000 usually
    if val < 1000:
        val += 5000
    return val

def parse_hebrew_date(day_text: str, month_text: str, year_text: str):
    """
    Convert Hebrew textual date into (year, month, day).
    Example: כ"ט, אדר א', תשס"ה → (5765, 6, 29)
    """
    day = hebrew_gematria_to_num(day_text)
    year = hebrew_year_to_num(year_text)
    
    # Normalize month name
    month_text = month_text.replace("באדר", "אדר").replace(" ", "")
    if month_text in HEBREW_MONTHS:
        month = HEBREW_MONTHS[month_text]
    else:
        raise ValueError(f"Unknown month: {month_text}")

    return year, month, day

