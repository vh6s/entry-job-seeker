from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from extensions import extract_technologies
from extensions.date_formatter import parse_published_date
from model import JobListing, JobOffer

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

    def scrape(self) -> list[JobListing]:
        job_listings = []
        current_url = self.start_url

        while current_url:
            response = self.session.get(current_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            job_listings.extend(self._extract_job_listings(soup))

            next_button = soup.select_one("a.Pagination__button--next")

            if next_button:
                current_url = urljoin(self.BASE_URL, next_button["href"])
            else:
                current_url = None
                
            print(current_url)
            
        return job_listings
    
    '''
    
    '''
    def _extract_job_listings(self, soup: BeautifulSoup) -> list[JobListing]:
        job_listings = []
        
        for card in soup.select("article.SearchResultCard"):
            link = card.select_one("a.SearchResultCard__titleLink")
            
            if not link or not (href := link.get("href")):
                continue
            
            title = link.get_text(strip=True)
            
            company_element = card.select(".SearchResultCard__footerItem")[0]
            company = company_element.get_text(strip=True)
            
            location_element = card.select_one("[data-test='serp-locality']")
            location = location_element.get_text(strip=True) if location_element else ""
            
            date_element = card.select_one(".SearchResultCard__status")
            published = (parse_published_date(date_element.get_text(strip=True)) if date_element else None)
                
            job_listings.append(
                JobListing(
                    title = title,
                    company = company,
                    location = location,
                    published = published,
                    url = urljoin(self.BASE_URL, href))
            )
            
        return job_listings

    
    def parse_job(self, listing: JobListing) ->  JobOffer:
        response = self.session.get(listing.url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        
        # if location present on the detail page, we take that exact address, otherwise we use fallback location area from the listing
        location_element = soup.select_one("[data-test='jd-info-location']")
        detail_location = (location_element.get_text(strip=True) if location_element else None)
        location = detail_location or listing.location
        
        # extracted description if element exists, added a new line between paragraphs
        description_element = soup.select_one("[data-test='jd-body-richtext']")
        description = (description_element.get_text("\n", strip=True) if description_element else "")
        
        technologies = extract_technologies(description)
        
        return JobOffer(
            company=listing.company,
            location=location,
            title=listing.title,
            description=description,
            technologies=technologies,
            published=listing.published,
            source="jobs.cz",
            url=listing.url
        )