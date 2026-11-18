"""
Runs the real scraper against a public test site and writes the result to a local CSV,
so you can open and see the actual scraped data without needing a Google service account.
"""
import csv
from main import scrape_products

if __name__ == "__main__":
    url = "https://books.toscrape.com/"
    rows = scrape_products(url)

    with open("scraped_output.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price", "url"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Scraped {len(rows)} rows -> scraped_output.csv")
