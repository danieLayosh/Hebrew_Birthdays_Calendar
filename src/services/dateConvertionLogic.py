from pyluach import dates

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