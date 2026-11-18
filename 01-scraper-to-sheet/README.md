# Scraper → Google Sheet

Scrapes product listings (name/price/url) from a search results page and writes them to a Google Sheet.

## Setup
1. `pip install -r requirements.txt && playwright install chromium`
2. Create a Google Cloud service account, download its JSON key as `service_account.json` in this folder, share the target Sheet with the service account's email.
3. Edit the CSS selectors in `scrape_products()` to match the target site's DOM.

## Note on Shopee/Lazada
Shopee's search page returns a CAPTCHA to headless Playwright directly — real client jobs on these sites need either their public API, a logged-in session with cookies, or a headless-detection bypass (stealth plugin / residential proxy). `test_scrape.py` currently points at books.toscrape.com to prove the scrape → data pipeline works end to end; swap the URL and selectors in `main.py` once you have a workable approach for the target site.

## Run
```
python main.py "https://shopee.co.th/search?keyword=..." <SHEET_ID> <WORKSHEET_NAME>
```

## Portfolio pitch
"Pulls live product data from an e-commerce search page into a Google Sheet on demand — buyer price-monitoring, competitor tracking, inventory lists."
