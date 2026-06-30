from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from extensions.extract_technologies import extract_technologies
from extensions.date_formatter import parse_published_date
from model.JobListing import JobListing
from model.JobOffer import JobOffer


class PraceCZScraper:
    BASE_URL = "https://www.prace.cz"

    def __init__(self, start_url: str):
        self.start_url = start_url

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
            )
        })

    def scrape(self) -> list[JobListing]:
        job_listings = []
        current_url = self.start_url

        while current_url:
            response = self.session.get(current_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # TODO add two separate parsers for default prace and custom page detail

            job_listings.extend(self._extract_job_listings(soup))

            next_button = soup.select_one("a[rel='next']")

            if next_button:
                current_url = urljoin(self.BASE_URL, next_button["href"])
            else:
                current_url = None

        return job_listings


    def _extract_job_listings(self, soup: BeautifulSoup) -> list[JobListing]:
        job_listings = []

        for card in soup.select("article[id^='advert-']"):
            link = card.select_one("[data-testid='advert-link']")

            if not link or not (href := link.get("href")):
                continue

            title = link.get_text(strip=True)
            company = (card.select(".typography-body-medium-regular.text-wrap-pretty")[0].get_text(strip=True))
            location = (card.select_one(".typography-body-medium-semibold").get_text(strip=True))

            job_listings.append(
                JobListing(
                    title=title,
                    company=company,
                    location=location,
                    published=None,
                    url=urljoin(self.BASE_URL, href))
            )

        return job_listings


    def parse_job(self, listing: JobListing) -> JobOffer:
        response = self.session.get(listing.url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        location_element = soup.select_one("[data-test='jd-info-location']")
        detail_location = (location_element.get_text(strip=True) if location_element else None)
        location = detail_location or listing.location

        description_element = soup.select_one("div[class*='RichContent']")
        description = (description_element.get_text("\n\n", strip=True) if description_element else "")

        technologies = extract_technologies(description)

        return JobOffer(
            company=listing.company,
            location=location,
            title=listing.title,
            description=description,
            technologies=technologies,
            published=listing.published,
            source="prace.cz",
            url=listing.url
        )





