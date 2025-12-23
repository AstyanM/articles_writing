import os
from firecrawl import Firecrawl
from dotenv import load_dotenv

load_dotenv()

class FirecrawlClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            print("Warning: FIRECRAWL_API_KEY missing in .env")
            self.app = None
            return

        try:
            # API Firecrawl v4.x
            self.app = Firecrawl(api_key=self.api_key)
        except Exception as e:
            print(f"Failed to initialize Firecrawl: {e}")
            self.app = None

    def scrape_url(self, url: str) -> str:
        if not self.app:
            return ""

        try:
            result = self.app.scrape(
                url,
                formats=["markdown"]
            )

            if isinstance(result, dict):
                return result.get("markdown", "")

            return str(result)

        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return ""
