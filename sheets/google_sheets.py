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
        if not offers:
            return
        
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
        jobs.sort(key=lambda row: row[7], reverse=True)
    
        self.sh.insert_rows(jobs, row = 3)
        self._copy_checkboxes_to_last_row(len(jobs))
        
    
    def _copy_checkboxes_to_last_row(self, count: int) -> None:
        requests = []

        for i in range(count):
            requests.append({
                "copyPaste": {
                    "source": {
                        "sheetId": self.sh.id,
                        "startRowIndex": 1,
                        "endRowIndex": 2,
                        "startColumnIndex": 3,
                        "endColumnIndex": 6,
                    },
                    "destination": {
                        "sheetId": self.sh.id,
                        "startRowIndex": 2 + i,
                        "endRowIndex": 3 + i,
                        "startColumnIndex": 3,
                        "endColumnIndex": 6,
                    },
                    "pasteType": "PASTE_NORMAL",
                }
            })

        self.sh.spreadsheet.batch_update({"requests": requests})