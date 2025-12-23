from src.search import SerperClient
import sys
import os
import json

# Add src to path
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'src')))


def main():
    print("Testing SerperClient...")

    try:
        client = SerperClient()
    except ValueError as e:
        print(f"Setup Error: {e}")
        print("Please create a .env file with SERPER_API_KEY")
        return

    # Using 'qdr:d' (past 24h) to ensure we get very recent results
    # Use a query that likely has daily news, e.g., "AI news" or similar.
    query = "parcoursup inscriptions"
    date_filter = "d"  # Last day

    print(f"Searching for: '{query}' with filter qdr:{date_filter}...")

    # We will search for 3 results
    results = client.search(query, date_range=date_filter, num_results=3)

    if not results:
        print("No results returned or error occurred.")
        return

    print("\n--- Results ---")

    if 'organic' in results:
        for i, item in enumerate(results['organic'], 1):
            title = item.get('title', 'No Title')
            link = item.get('link', 'No Link')
            date = item.get('date', 'No Date')
            snippet = item.get('snippet', 'No snippet')

            print(f"[{i}] {title}")
            print(f"    Date: {date}")
            print(f"    Link: {link}")
            print(f"    Snippet: {snippet[:100]}...")
            print("-" * 30)
    else:
        print("No organic results found in response.")
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
