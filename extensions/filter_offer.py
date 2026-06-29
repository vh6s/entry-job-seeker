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
    "konzultant",
    "úklid",
    "stavebnictví",
}

def is_relevant(offer: JobOffer) -> bool:
    title = offer.title.lower()
    
    if any(keyword in title for keyword in EXCLUDED_TITLE_KEYWORDS):
        return False
    
    if not offer.technologies:
        return False
    
    return True