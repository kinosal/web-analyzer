"Process list of urls and save corresponding artists."

# Import from standard library
import sys
import csv
import time
import re
from typing import Dict

# Import app factory, modules and models
from app import create_app
import app.config as config

import app.scripts.comprehend as com
import app.scripts.scrape as scr
import app.scripts.metafire as met
import app.scripts.spotify as spo

from app.models.models import Url as UrlModel
from app.models.models import save_url

# Create app and push context to access db
app = create_app(config.set_config())
app.app_context().push()


class BulkProcessor:
    def __init__(self, source: str = "metafire"):
        self.scraper = scr.Scraper()
        self.comprehender = com.Comprehend()
        self.source = source
        if source == "metafire":
            self.finder = met.Metafire()
        elif source == "spotify":
            self.finder = spo.Spotify()

    def process_url(self, url: str) -> str:
        if UrlModel.query.filter(UrlModel.url == url).first():
            return "exists"

        response = self.scraper.request_url(url)
        if not response:
            return "bad url"

        path = " ".join(re.split('/|-|_', url)[3:])
        content = self.scraper.extract_content(response)
        text = (path + " " + content)[:1000]
        language = self.comprehender.language(text)
        if language in self.comprehender.comprehender_languages:
            entities = self.comprehender.entities(text, language)
        elif language in self.comprehender.translater_languages:
            content = self.comprehender.translate(text, language, "en")
            entities = self.comprehender.entities(text, "en")
        else:
            return "language not supported"

        artists = []
        for e in entities:
            artists = self.finder.find_artists(e["text"], score=True)
            if artists:
                break

        if not artists:
            return "no artist found"

        save_url(url, self.source, artists[0])
        return "created"

    def save_from_csv(self, path: str, limit: int = 10) -> None:
        with open(path, mode="r") as file:
            csv_reader = csv.DictReader(file)
            domain_counts: Dict[str, int] = {}
            line_count = 0
            created_count = 0
            for row in csv_reader:
                line_count += 1

                if line_count > 1:
                    try:
                        domain = row["url"].split("/")[2]
                    except IndexError:
                        continue

                    if (
                        domain in domain_counts.keys()
                        and domain_counts[domain] > 1.5
                        * sum(domain_counts.values()) / len(domain_counts.keys())
                    ):
                        continue

                    response = self.process_url(row["url"])

                    if response in ["created", "exists"]:
                        if domain in domain_counts.keys():
                            domain_counts[domain] += 1
                        else:
                            domain_counts[domain] = 1

                    if response == "created":
                        created_count += 1
                        print(f"Created {row['url']}")
                        time.sleep(0.5)

                if sum(domain_counts.values()) >= limit:
                    break

            print(
                f"Processed {line_count} urls, created {created_count}, "
                f"{sum(domain_counts.values())} exist"
            )


if __name__ == '__main__':
    processor = BulkProcessor(sys.argv[3])
    processor.save_from_csv(path=sys.argv[1], limit=int(sys.argv[2]))
