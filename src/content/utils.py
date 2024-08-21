from datetime import datetime

def datetime_to_str(date: datetime):
    if not date:
        return None

    return date.strftime('%Y-%m-%d %H:%M:%S')
