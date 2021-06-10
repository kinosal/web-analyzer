"Process list of urls and save corresponding artists."

# Import from standard library
import sys
import csv
import time

# Import app factory, modules and models
from app import create_app
import app.config as config

import app.scripts.comprehend as com
import app.scripts.scrape as scr
import app.scripts.spotify as spo

from app.models.models import Url as UrlModel
from app.models.models import save_url

# Create app and push context to access db
app = create_app(config.set_config())
app.app_context().push()


class BulkProcessor:
    scraper = scr.Scraper()
    comprehender = com.Comprehend()
    spotify = spo.Spotify()

    def process_url(self, url: str) -> str:
        if UrlModel.query.filter(UrlModel.url == url).first():
            return "exists"

        response = self.scraper.request_url(url)
        if not response:
            return "bad url"

        content = self.scraper.extract_content(response)
        language = self.comprehender.language(content[:2500])
        entities = self.comprehender.entities(content[:2500], language)
        for e in entities:
            artists = self.spotify.find_artists(e["text"])
            if artists:
                break

        if not artists:
            return "no artist found"

        artist = {
            "name": artists[0]["name"],
            "popularity": artists[0]["popularity"],
            "external_id": artists[0]["id"],
        }
        if artist:
            save_url(url, "spotify", artist)

        time.sleep(1)
        return "created"

    def save_from_csv(self, path: str, limit: int = 10) -> None:
        with open(path, mode="r") as file:
            csv_reader = csv.DictReader(file)
            line_count = 0
            created_count = 0
            for row in csv_reader:
                if line_count > 0:
                    response = self.process_url(row["url"])
                    if response == "created":
                        created_count += 1
                line_count += 1
                print(f"Processed {row['url']}")
                if line_count >= limit:
                    break

            print(f"Processed {line_count} urls, created {created_count}")


if __name__ == '__main__':
    processor = BulkProcessor()
    processor.save_from_csv(path=sys.argv[1], limit=int(sys.argv[2]))
