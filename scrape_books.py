"""Scrape all books from books.toscrape.com and save to CSV."""

import csv
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
TOTAL_PAGES = 50
DELAY_SECONDS = 1
OUTPUT_FILE = "books_dataset.csv"

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def page_url(page_num: int) -> str:
    if page_num == 1:
        return BASE_URL
    return urljoin(BASE_URL, f"catalogue/page-{page_num}.html")


def parse_rating(star_rating_tag) -> int | None:
    if star_rating_tag is None:
        return None
    classes = star_rating_tag.get("class", [])
    for name in classes:
        if name in RATING_MAP:
            return RATING_MAP[name]
    return None


def scrape_page(session: requests.Session, page_num: int) -> list[dict]:
    response = session.get(page_url(page_num), timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    books = []

    for article in soup.select("article.product_pod"):
        title_tag = article.select_one("h3 a")
        price_tag = article.select_one("p.price_color")
        availability_tag = article.select_one("p.instock.availability")
        rating_tag = article.select_one("p.star-rating")

        books.append(
            {
                "title": title_tag.get("title", "").strip()
                if title_tag
                else "",
                "price": price_tag.get_text(strip=True) if price_tag else "",
                "rating": parse_rating(rating_tag),
                "availability": availability_tag.get_text(strip=True)
                if availability_tag
                else "",
            }
        )

    return books


def main() -> None:
    all_books: list[dict] = []

    with requests.Session() as session:
        session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (compatible; BooksScraper/1.0; "
                    "+https://books.toscrape.com)"
                )
            }
        )

        for page_num in range(1, TOTAL_PAGES + 1):
            books = scrape_page(session, page_num)
            all_books.extend(books)
            print(
                f"Page {page_num}/{TOTAL_PAGES}: "
                f"scraped {len(books)} books "
                f"(total so far: {len(all_books)})"
            )

            if page_num < TOTAL_PAGES:
                time.sleep(DELAY_SECONDS)

    fieldnames = ["title", "price", "rating", "availability"]
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_books)

    print(f"\nDone. Wrote {len(all_books)} books to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
