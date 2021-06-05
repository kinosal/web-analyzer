"""Web content scraper."""

# Import from standard library
import requests
import random

# Import from 3rd party libraries
from bs4 import BeautifulSoup


class Scraper:
    """Simple web scraper."""

    AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/68.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/68.0",
    ]

    agent = AGENTS[random.randint(0, len(AGENTS) - 1)]

    @staticmethod
    def set_option(options, current):
        """Helper function to select next option list element."""
        i = options.index(current)
        return options[0] if i + 1 == len(options) else options[i + 1]

    def switch_agent(self) -> None:
        """Switch to next agent to avoid blocking."""
        self.agent = self.set_option(self.AGENTS, self.agent)

    def request_url(self, url, timeout=10) -> requests.Response:
        """Request URL with agent."""
        response = requests.get(
            url,
            headers={"User-Agent": self.agent, "Connection": "close"},
            timeout=timeout,
        )
        self.switch_agent()
        return response

    @staticmethod
    def extract_content(html: requests.Response) -> str:
        """Extract plain text from html."""
        soup = BeautifulSoup(html.text, "html.parser").text
        return " ".join(soup.split())
