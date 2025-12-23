from src.analysis import ContentAnalyzer
from src.scraper import FirecrawlClient
from src.search import SerperClient
import sys
import os
import json
from dotenv import load_dotenv


def main():
    load_dotenv()

    # 1. Configuration
    query = "Concours Geipi Polytech 2025 dates"  # Example query
    angle_focus = "Les nouvelles épreuves écrites et astuces de révision"

    print(f"--- STEP 1: Searching for '{query}' ---")
    serper = SerperClient()
    # Get top 5 from last month
    results = serper.search(query, date_range='m', num_results=5)

    if not results or 'organic' not in results:
        print("No search results found.")
        return

    urls_to_scrape = [item['link']
                      for item in results['organic'] if 'link' in item]
    print(f"Found {len(urls_to_scrape)} URLs.")

    # 2. Scraping
    print("\n--- STEP 2: Scraping content ---")
    firecrawl = FirecrawlClient()
    contents = []

    for url in urls_to_scrape[:3]:  # Limit to top 3 for cost/speed
        print(f"Scraping: {url}")
        content = firecrawl.scrape_url(url)
        if content:
            contents.append(content)
        else:
            print(f"Failed to scrape {url}")

    if not contents:
        print("No content could be scraped.")
        return

    # 3. Analysis
    print("\n--- STEP 3: Analysing content ---")
    analyzer = ContentAnalyzer()
    analysis_result = analyzer.analyze_competitors(
        contents, angle_focus=angle_focus)

    print("\n=== ANALYSIS RESULT ===")
    print(analysis_result)

    # Save result
    with open("analysis_result.md", "w", encoding="utf-8") as f:
        f.write(analysis_result)
    print("\nResult saved to analysis_result.md")


if __name__ == "__main__":
    main()
