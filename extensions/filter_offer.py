from extensions.extract_technologies import KNOWN_TECHNOLOGIES as technologies
from model import JobOffer

CORE_TECHNOLOGIES = {
    "python",
    "java",
    "javascript",
    "typescript",
    "react",
    "django",
    "flask",
    "fastapi",
    "sql",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "databricks",
    "node.js",
    "nodejs",
}

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
    
    if not any(tech in CORE_TECHNOLOGIES for tech in offer.technologies):
        return False
    
    return True