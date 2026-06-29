import requests
from credentials.discord_webhook import DISCORD_WEBHOOK
from model.JobOffer import JobOffer


class DiscordNotification:
    def __init__(self):
        self.webhook_url = DISCORD_WEBHOOK
    
    def send_notification(self, jobs: list[JobOffer]) -> None:
        if not jobs:
            return

        lines = [f"• **{job.title}** - {job.company} - [link]({job.url})" for job in jobs]

        message = (f"## {len(jobs)} new job(s) found\n\n" + "\n".join(lines))

        response = requests.post(
            self.webhook_url,
            json={
                "content": message
            },
            timeout=10,
        )
        response.raise_for_status()