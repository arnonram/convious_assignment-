from datetime import date, timedelta


def today(formatted=True):
    today = date.today()
    return format_date(today) if formatted else today


def format_date(date):
    return date.strftime("%Y-%m-%d")


def past_date(day_ago: int, formatted=True):
    new_date = today(False) - timedelta(days=day_ago)
    return format_date(new_date) if formatted else new_date
