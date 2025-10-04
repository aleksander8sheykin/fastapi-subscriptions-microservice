from datetime import date


def parse_month_year(value: str | date) -> date | None:
    if value is None:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        value = value.strip()
        try:
            month, year = map(int, value.split("-"))
            return date(year, month, 1)
        except Exception as err:
            raise ValueError(f"Invalid month-year format: {value!r}") from err
    raise ValueError(f"Cannot parse date from {value!r}")
