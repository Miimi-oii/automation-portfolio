"""
Scrape product listings from a search result page and push rows to a Google Sheet.
Usage: python main.py "<search_url>" <sheet_id> <worksheet_name>
"""
import sys
import gspread
from google.oauth2.service_account import Credentials
from playwright.sync_api import sync_playwright

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def scrape_products(search_url: str) -> list[dict]:
    rows = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(search_url, wait_until="networkidle")

        # TODO: swap selectors for the target site (Shopee/Lazada/etc.)
        cards = page.query_selector_all("article.product_pod")
        for card in cards:
            name_el = card.query_selector("h3 a")
            price_el = card.query_selector(".price_color")
            rows.append({
                "name": name_el.get_attribute("title") if name_el else "",
                "price": price_el.inner_text() if price_el else "",
                "url": name_el.get_attribute("href") if name_el else "",
            })
        browser.close()
    return rows


def push_to_sheet(rows: list[dict], sheet_id: str, worksheet_name: str) -> None:
    creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).worksheet(worksheet_name)

    sheet.clear()
    if not rows:
        return
    headers = list(rows[0].keys())
    sheet.append_row(headers)
    for row in rows:
        sheet.append_row([row[h] for h in headers])


if __name__ == "__main__":
    search_url, sheet_id, worksheet_name = sys.argv[1], sys.argv[2], sys.argv[3]
    products = scrape_products(search_url)
    push_to_sheet(products, sheet_id, worksheet_name)
    print(f"Pushed {len(products)} rows to '{worksheet_name}'")
