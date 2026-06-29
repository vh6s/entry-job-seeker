from dataclasses import dataclass
from datetime import date


@dataclass
class JobListing:
    title: str
    company: str
    location: str
    published: date | None
    url: str