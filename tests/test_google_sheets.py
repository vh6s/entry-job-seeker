from datetime import date
from model import JobOffer
from sheets.google_sheets import GoogleSheets


def main() -> None:
    print("1")

    sheets = GoogleSheets()

    print("2")

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

    print("3")

    sheets.append_offer([offer])

    print("4")


if __name__ == "__main__":
    main()