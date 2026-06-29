
from dataclasses import dataclass
from datetime import date

# data model that represents each column in the google sheet
@dataclass
class JobOffer:
    company: str
    location: str
    title: str
    description: str
    technologies: list[str]
    published: date | None
    source: str
    url: str