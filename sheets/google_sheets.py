import gspread
from credentials.spreadsheet import SPREADSHEET_URL, WORKSHEET_NAME
from model import JobOffer

class GoogleSheets:
    def __init__(self):
        self.gc = gspread.service_account(filename="credentials/service_account.json")
        self.sh = self.gc.open_by_key(SPREADSHEET_URL).worksheet(WORKSHEET_NAME)
    
    def get_existing_urls(self) -> set[str]:
        urls = self.sh.col_values(10)
        return set(urls[1:])
       
     
    def append_offer(self, offers: list[JobOffer]) -> None:
        jobs = []
        
        for job in offers:
            jobs.append([
                job.company,
                job.location,
                job.title,
                "",
                "",
                "",
                ", ".join(job.technologies),
                job.published.isoformat() if job.published else "",
                job.source,
                job.url,
                job.description,
            ])
    
        self.sh.append_rows(jobs)