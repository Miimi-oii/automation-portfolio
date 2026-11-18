from main import scrape_products

if __name__ == "__main__":
    url = "https://books.toscrape.com/"
    rows = scrape_products(url)
    print(f"Found {len(rows)} rows")
    for r in rows[:5]:
        print(r)
