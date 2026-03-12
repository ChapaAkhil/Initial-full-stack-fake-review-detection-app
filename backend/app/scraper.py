import re
from typing import List, Tuple, Dict, Optional
from urllib.parse import urlparse, urlunparse, urlencode

import requests
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/121.0 Safari/537.36"
)


class ScrapeError(Exception):
    pass


def _marketplace_name(product_url: str) -> Optional[str]:
    netloc = urlparse(product_url).netloc.lower()
    if "amazon." in netloc or "amzn." in netloc:
        return "Amazon"
    if "flipkart" in netloc:
        return "Flipkart"
    if "myntra" in netloc:
        return "Myntra"
    if "ajio" in netloc:
        return "Ajio"
    return None


def extract_asin(url: str) -> Optional[str]:
    patterns = [
        r"/dp/([A-Z0-9]{10})",
        r"/gp/product/([A-Z0-9]{10})",
        r"/gp/aw/d/([A-Z0-9]{10})",
        r"/product-reviews/([A-Z0-9]{10})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            return match.group(1).upper()
    return None


def build_reviews_url(product_url: str, page: int) -> str:
    asin = extract_asin(product_url)
    if not asin:
        raise ScrapeError("Could not extract ASIN from the provided URL.")

    parsed = urlparse(product_url)
    scheme = parsed.scheme or "https"
    netloc = parsed.netloc or "www.amazon.com"

    path = f"/product-reviews/{asin}"
    query = urlencode({"pageNumber": page, "sortBy": "recent"})

    return urlunparse((scheme, netloc, path, "", query, ""))


def _safe_text(element) -> str:
    if not element:
        return ""
    return element.get_text(strip=True)


def _parse_rating(text: str) -> Optional[float]:
    match = re.search(r"([0-5](?:\.[0-9])?)", text)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def _parse_helpful(text: str) -> Tuple[int, int]:
    if not text:
        return 0, 0

    # Handles: "2 of 3 people found this helpful"
    match = re.search(r"(\d+)\s+of\s+(\d+)", text)
    if match:
        return int(match.group(1)), int(match.group(2))

    # Handles: "2 people found this helpful"
    match = re.search(r"(\d+)", text)
    if match:
        value = int(match.group(1))
        return value, value

    return 0, 0


def _parse_date(text: str):
    if not text:
        return None
    try:
        return date_parser.parse(text, fuzzy=True)
    except (ValueError, TypeError):
        return None


def fetch_reviews(product_url: str, max_pages: int = 5, timeout: int = 20) -> Tuple[List[Dict], str]:
    asin = extract_asin(product_url)
    if not asin:
        raise ScrapeError("Could not extract ASIN from the provided URL.")

    headers = {
        "User-Agent": USER_AGENT,
        "Accept-Language": "en-US,en;q=0.9",
    }

    all_reviews: List[Dict] = []
    marketplace = _marketplace_name(product_url)

    for page in range(1, max_pages + 1):
        url = build_reviews_url(product_url, page)
        response = requests.get(url, headers=headers, timeout=timeout)

        if response.status_code != 200:
            raise ScrapeError(f"Failed to fetch reviews page {page}. Status: {response.status_code}")

        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        review_blocks = soup.select('div[data-hook="review"]')

        if not review_blocks:
            if page == 1:
                lowered = html.lower()
                blocked_markers = [
                    "robot check",
                    "captcha",
                    "automated access",
                    "not a robot",
                    "sorry, we just need to make sure",
                    "enter the characters",
                ]
                if any(marker in lowered for marker in blocked_markers):
                    if marketplace:
                        raise ScrapeError(
                            f"{marketplace} blocked this request. Please use Manual Review Input."
                        )
                    raise ScrapeError(
                        "Scraping blocked by the marketplace. Please use Manual Review Input."
                    )
                if marketplace:
                    raise ScrapeError(
                        f"{marketplace} blocked this request. Please use Manual Review Input."
                    )
            break

        for block in review_blocks:
            review_text = _safe_text(block.select_one('span[data-hook="review-body"]'))

            rating_text = _safe_text(block.select_one('i[data-hook="review-star-rating"] span'))
            if not rating_text:
                rating_text = _safe_text(block.select_one('i[data-hook="cmps-review-star-rating"] span'))
            rating = _parse_rating(rating_text)

            helpful_text = _safe_text(block.select_one('span[data-hook="helpful-vote-statement"]'))
            helpful_num, helpful_den = _parse_helpful(helpful_text)

            date_text = _safe_text(block.select_one('span[data-hook="review-date"]'))
            timestamp = _parse_date(date_text)

            author_link = block.select_one('a[data-hook="review-author"]')
            reviewer_id = _safe_text(author_link)
            if author_link and author_link.has_attr("href"):
                match = re.search(r"/gp/profile/([^/]+)", author_link["href"])
                if match:
                    reviewer_id = match.group(1)

            if review_text:
                all_reviews.append({
                    "review_text": review_text,
                    "rating": rating,
                    "helpfulness_numerator": helpful_num,
                    "helpfulness_denominator": helpful_den,
                    "timestamp": timestamp,
                    "reviewer_id": reviewer_id,
                    "product_id": asin,
                })

    return all_reviews, asin
