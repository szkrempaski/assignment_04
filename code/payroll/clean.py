
import pandas as pd
def parse_hours(value) -> float:
    """...(keep the starter docstring)..."""
    if pd.isna(value):
        return 0.0
    if not isinstance(value, str):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    text = value.strip().lower()
    if not text:
        return 0.0

    if "h" not in text and "m" not in text:
        try:
            return float(text)
        except ValueError:
            return 0.0

    hours = 0.0
    try:
        for word in text.split():
            if word.endswith("h"):
                hours += float(word[:-1])
            elif word.endswith("m"):
                hours += float(word[:-1]) / 60
            else:
                return 0.0
    except ValueError:
        return 0.0
    return hours


def clean_currency(value) -> float:
    """...(keep the starter docstring)..."""
    if pd.isna(value):
        return 0.0
    if not isinstance(value, str):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    text = value.replace("$", "").replace(",", "").strip()
    try:
        return float(text)
    except ValueError:
        return 0.0


def add_hours_worked(timesheet: pd.DataFrame) -> pd.DataFrame:
    """...(keep the starter docstring)..."""
    out = timesheet.copy()
    out["hours_worked"] = out["hours"].apply(parse_hours)
    return out


def add_hourly_rate(employees: pd.DataFrame) -> pd.DataFrame:
    """...(keep the starter docstring)..."""
    out = employees.copy()
    out["hourly_rate_usd"] = out["hourly_rate"].apply(clean_currency)
    return out