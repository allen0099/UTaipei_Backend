from datetime import date


def get_semester() -> int:
    today = date.today()
    return 1 if today.month > 6 else 2
