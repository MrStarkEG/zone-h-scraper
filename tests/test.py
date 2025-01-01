from bs4 import BeautifulSoup

file = open(r"tests\test.html", "r", encoding="utf-8")

html_content = file.read()


def scrape_interface(html_content, section_name):
    soup = BeautifulSoup(html_content, "html.parser")
    all_rows = soup.find_all("tr")[1:-2]

    for row in all_rows:

        # Extract desired information
        time = row.find_all("td")[0].text.strip()
        notifier_name = row.find_all("td")[1].find("a").text.strip()
        domain = row.find_all("td")[7].text.strip()
        os = row.find_all("td")[8].text.strip()
        mirror_href = row.find_all("td")[9].find("a")["href"]

        # Extract the country name from the <img> tag
        country_img = row.find_all("td")[5].find("img")
        country = country_img["alt"].strip() if country_img else "Unknown"

        data = {
            "time": time,
            "notifier_name": notifier_name,
            "domain": domain,
            "os": os,
            "country": country,
            "mirror_href": mirror_href,
            "section": section_name
        }

        print(data)


def find_href_after_strong(html_content):
    """
    Find the href of the <a> tag that comes immediately after a <strong> tag.

    Args:
        html_content (str): The HTML content as a string.

    Returns:
        str: The href of the <a> tag if found, else None.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    strong_tag = soup.find("strong")
    if strong_tag:
        next_a_tag = strong_tag.find_next_sibling("a")
        if next_a_tag and "href" in next_a_tag.attrs:
            return next_a_tag["href"]

    return None


# scrape_interface(html_content, "archive")

print(find_href_after_strong(html_content))
