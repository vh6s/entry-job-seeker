from extensions.filter_offer import is_relevant
from notifications.discord import DiscordNotification
from scrapers.jobscz import JobsCZScraper
from sheets.google_sheets import GoogleSheets


def main():
    jobsScraper = JobsCZScraper("https://www.jobs.cz/brigady/?locality%5B0%5D%5Bcode%5D=M265747&locality%5B0%5D%5Blabel%5D=Brno&locality%5B0%5D%5Bcoords%5D=49.19186,16.61108&locality%5B0%5D%5Bradius%5D=10")
    notifier = DiscordNotification()
    sheets = GoogleSheets()
    
    existing_urls = sheets.get_existing_urls()
    new_jobs = []
    
    for listing in jobsScraper.scrape():
        offer = jobsScraper.parse_job(listing)
        
        if not is_relevant(offer):
            continue
        
        if offer.url in existing_urls:
            continue
        
        new_jobs.append(offer)
    
    sheets.append_offer(new_jobs)
    notifier.send_notification(new_jobs)


if __name__ == "__main__":
    main()
