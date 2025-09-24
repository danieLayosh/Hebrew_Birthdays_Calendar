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
    
