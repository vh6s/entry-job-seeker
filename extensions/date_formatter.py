from datetime import date, timedelta
import re

MONTHS = {
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

def parse_published_date(text: str) -> date | None:
        text = text.strip().lower()
        today = date.today()
        
        if "končí" in text:
            return None
        
        if "před" in text:
            return today

        if "dnes" in text:
            return today

        if "včera" in text:
            return today - timedelta(days=1)

        match = re.search(r'(\d+)\.\s*([a-zěščřžýáíéúů]+)', text)
        if match:
            day_str = match.group(1)
            month_name = match.group(2)
            
            if month_name in MONTHS:
                return date(
                    year=today.year,
                    month=MONTHS[month_name],
                    day=int(day_str),
                )
                
        return None