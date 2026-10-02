import requests
from bs4 import BeautifulSoup
import re
from typing import Dict

try:
    from .utils import save_to_json
except ImportError:
    from utils import save_to_json


HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; WikiScraper/1.0)"}


def fetch_wikipedia_page(url: str) -> str:
    """Fetch the HTML content of the given Wikipedia page."""
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.text


def extract_title(soup: BeautifulSoup) -> str:
    """Extract the title of the Wikipedia page."""
    heading = soup.find("h1", id="firstHeading")
    if heading:
        return heading.get_text(strip=True)
    if soup.title and soup.title.string:
        return soup.title.string.replace(" - Wikipedia", "").strip()
    return ""


def extract_first_sentence(soup: BeautifulSoup) -> str:
    """Extract the first sentence of the first paragraph on the Wikipedia page."""
    content = soup.find("div", id="mw-content-text") or soup
    for p in content.find_all("p"):
        # Видаляємо виноски на кшталт [1], [note 1]
        for sup in p.find_all("sup", class_="reference"):
            sup.decompose()
        text = p.get_text(" ", strip=True)
        if not text:
            continue  # пропускаємо порожні <p> (mw-empty-elt)
        text = re.sub(r"\s+([,.;:!?)])", r"\1", text)  # прибираємо зайві пробіли
        text = re.sub(r"\(\s+", "(", text)
        # Перше речення: до крапки, після якої йде пробіл і велика літера
        match = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text, maxsplit=1)
        return match[0].strip()
    return ""


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    try:
        page_content = fetch_wikipedia_page(url)
        soup = BeautifulSoup(page_content, 'html.parser')

        # Extract the title of the page
        title = extract_title(soup)

        # Extract the first sentence of the first paragraph
        first_sentence = extract_first_sentence(soup)

        # Combine the extracted data
        extracted_data = {
            "title": title,
            "first_sentence": first_sentence
        }

        # Print the extracted data
        print("Extracted Data:", extracted_data)

        # Save the data to a JSON file
        save_to_json(extracted_data, 'extracted_wikipedia_data.json')

        print("Data successfully saved to extracted_wikipedia_data.json")
    except Exception as e:
        print(f"An error occurred: {e}")
