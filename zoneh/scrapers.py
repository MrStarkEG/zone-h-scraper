from time import sleep
from bs4 import BeautifulSoup

from config import BASE_URL
from utils import find_href_after_strong
from helpers import convert_to_iso_format, save_to_jsonl_file


def scrape_interface(html_content, section_name):
    """
    Scrape the interface of the page and saves the results to a jsonl file.

    Args:
    -----
        html_content (str): The HTML content as a string.
        section_name (str): The name of the section being scraped.
    """

    soup = BeautifulSoup(html_content, "html.parser")
    all_rows = soup.find_all("tr")[1:-2]

    for row in all_rows:
        # Extract desired information
        time = row.find_all("td")[0].text.strip()
        notifier_url = row.find_all('td')[1].find('a')['href']
        notifier_name = row.find_all("td")[1].find("a").text.strip()
        domain = row.find_all("td")[7].text.strip()
        os = row.find_all("td")[8].text.strip()
        mirror_href = row.find_all("td")[9].find("a")["href"]

        # Extract the country name from the <img> tag
        country_img = row.find_all("td")[5].find("img")
        country = country_img["alt"].strip() if country_img else "Unknown"

        data = {
            "section": section_name,
            "domain": domain,
            "time": convert_to_iso_format(time),
            "notifier_name": BASE_URL + notifier_name,
            "notifier_url": notifier_url,
            "country": country,
            "os": os,
            "mirror_href": BASE_URL + mirror_href,
        }

        save_to_jsonl_file(data)


def default_scraper(session, url, section_name):
    """The default inhertited scraper for the sections of Zone-H."""

    while True:
        html_content = session.get(url).text
        scrape_interface(html_content, section_name)

        next_page_href = find_href_after_strong(html_content)

        if next_page_href:
            url = next_page_href
            print(f"Scraping next page: {url}")
            sleep(2)
        else:
            break

    print(f"Scraping complete for {section_name} section.")


def scrape_archive_section(session):
    """Scrape the archive section of Zone-H."""

    url = "https://www.zone-h.org/archive"

    section_name = 'archive'

    default_scraper(session, url, section_name)


def scrape_archive_star_section(session):
    """Scrape the archive star section of Zone-H."""

    url = "https://www.zone-h.org/archive/special=1"

    section_name = 'archive_star'

    default_scraper(session, url, section_name)


def scrape_onold_section(session):
    """Scrape the onhold section of Zone-H."""

    url = "https://www.zone-h.org/archive/published=0"

    section_name = 'onhold'

    default_scraper(session, url, section_name)
