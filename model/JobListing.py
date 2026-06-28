from dataclasses import dataclass
from datetime import date


@dataclass
class JobListing:
    url: str
    published: date | None