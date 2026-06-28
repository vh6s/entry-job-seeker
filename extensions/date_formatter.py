from datetime import date, timedelta

_MONTHS = {
    "ledna": 1,
    "února": 2,
    "března": 3,
    "dubna": 4,
    "května": 5,
    "června": 6,
    "července": 7,
    "srpna": 8,
    "září": 9,
    "října": 10,
    "listopadu": 11,
    "prosince": 12,
}

def parse_published_date(self, text: str) -> date | None:
        
        text = text.strip().lower()

        today = date.today()

        if text == "dnes":
            return today

        if text == "včera":
            return today - timedelta(days=1)

        try:
            day_str, month_name = text.replace(".", "").split()

            return date(
                year=today.year,
                month=_MONTHS[month_name],
                day=int(day_str),
            )

        except (ValueError, KeyError):
            return None