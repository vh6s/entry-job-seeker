from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

class JobsCZScraper:
    BASE_URL = "https://www.jobs.cz"

    def __init__(self, start_url: str):
        self.start_url = start_url

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
            )
        })

    def scrape(self) -> list[str]:
        job_urls = []
        current_url = self.start_url

        while current_url:
            response = self.session.get(current_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # TODO: Extract all job URLs from this page
            # job_urls.extend(...)

            next_button = soup.select_one("a.Pagination__button--next")

            if next_button:
                current_url = urljoin(
                    self.BASE_URL,
                    next_button["href"]
                )
            else:
                current_url = None
                
            print(current_url)

        return job_urls