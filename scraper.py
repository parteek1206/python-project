"""Web scraping module: fetches book data from books.toscrape.com."""
import logging
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

PAGE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
HEADERS = {"User-Agent": "Mozilla/5.0 (Student Mini Project)"}


class ScrapeError(Exception):
    """Raised when a page cannot be fetched."""


def parse_price(text):
    """Extract numeric price from string."""
    match = re.search(r"\d+(?:\.\d+)?", text)
    if not match:
        raise ValueError(f"No price found in: {text!r}")
    return float(match.group())


def parse_book(article, page_url):
    link = article.h3.a
    avail_text = article.select_one("p.availability").get_text(strip=True)
    in_stock = 1 if "In stock" in avail_text else 0

    img_tag = article.select_one("img.thumbnail")
    img_url = urljoin(page_url, img_tag["src"]) if img_tag else ""

    return {
        "title": link["title"],
        "price": parse_price(article.select_one("p.price_color").text),
        "rating": RATING_MAP.get(article.select_one("p.star-rating")["class"][1], 0),
        "in_stock": in_stock,
        "image_url": img_url,
        "url": urljoin(page_url, link["href"]),
    }


def fetch_page(url, timeout=10):
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        response.encoding = "utf-8"
        return response.text
    except requests.exceptions.RequestException as err:
        raise ScrapeError(f"Could not fetch {url}: {err}") from err


def scrape_books(max_pages=3, delay=0.5):
    books = []
    for page in range(1, max_pages + 1):
        url = PAGE_URL.format(page)
        html = fetch_page(url)
        if html is None:
            break
        soup = BeautifulSoup(html, "html.parser")
        for article in soup.select("article.product_pod"):
            try:
                books.append(parse_book(article, url))
            except (ValueError, KeyError, AttributeError, TypeError) as err:
                logging.warning("Skipped a book on page %s: %s", page, err)
        time.sleep(delay)
    return books