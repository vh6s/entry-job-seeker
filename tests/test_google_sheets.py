from datetime import date
from model.JobOffer import JobOffer
from sheets.google_sheets import GoogleSheets


def main() -> None:
    sheets = GoogleSheets()

    offer = JobOffer(
        company="Test Company",
        location="Brno",
        title="Google Sheets Integration Test",
        description="This row was added by a manual integration test.",
        technologies=["python", "sql"],
        published=date.today(),
        source="jobs.cz",
        url="https://example.com/test"
    )
    
    sheets.append_offer([offer])

if __name__ == "__main__":
    main()