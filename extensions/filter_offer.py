

from extensions.extract_technologies import KNOWN_TECHNOLOGIES as technologies
from model import JobOffer


EXCLUDED_TITLE_KEYWORDS = {
    "senior",
    "lead",
    "director",
    "sales",
    "obchodní",
    "řidič",
    "skladník",
}

def is_relevant(offer: JobOffer) -> bool:
    title = offer.title.lower()
    
    if any(keyword in title for keyword in EXCLUDED_TITLE_KEYWORDS):
        return False
    
    if not any(tech in technologies for tech in offer.technologies):
        return False
    
    return True