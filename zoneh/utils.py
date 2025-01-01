from bs4 import BeautifulSoup
from playwright.sync_api import Page
from config import BASE_URL


def get_existing_cookies():
    """
    Has default Cookies to start our journey.
    It is valid until 2026.
    We start our login with it to make it recognizable by the server -
        so it doesn't ask for a captcha -
            at the login page.
    """

    cookies = {
        'ZHE': 'e23d5dc70ab48f71fb062a456482c611',
        'PHPSESSID': 'rkhn0irffnfk0007f20btf5l25'
    }

    desired_cookies_string = "; ".join(
        f"{name}={value}" for name, value in cookies.items())

    print(desired_cookies_string)

    return desired_cookies_string


def convert_cookies(requests_cookies, domain: str = 'www.zone-h.org'):
    """
    Getting the cookies prepared in a specific format for Playwright -
        to be added to the browser context in order to be recognizable by the server.

    Args:
        requests_cookies (dict): The cookies in requests format.
        domain (str): The domain of the cookies and in our case the default one.

    Returns:
        list: The cookies in Playwright format.

    Note:
        I used 'EditThisCookie' extension in Chrome to get the cookies.
    """
    return [
        {
            "name": name,
            "value": value,
            "domain": domain,
            "path": "/",
            "httpOnly": True,
            "secure": False,
        }
        for name, value in requests_cookies.items()
    ]


def find_href_after_strong(html_content):
    """
    Find the href of the <a> tag that comes immediately after a <strong> tag -
        to know that if there is a next page to scrape of not.

    Args:
        html_content (str): The HTML content of the current pagination.

    Returns:
        str: The href of the <a> tag if found, else None.
    """

    soup = BeautifulSoup(html_content, "html.parser")

    strong_tag = soup.find("strong")
    if strong_tag:
        next_a_tag = strong_tag.find_next_sibling("a")
        if next_a_tag and "href" in next_a_tag.attrs:
            return BASE_URL + next_a_tag["href"]

    return None


def add_playwright_cookies_to_requests(session, playwright_cookies):
    """
    Add Playwright cookies to an existing requests.Session.

    Args:
        session (requests.Session): The existing requests session.
        playwright_cookies (list): List of cookies in Playwright format.
    """
    for cookie in playwright_cookies:

        domain = cookie["domain"].lstrip(".")

        session.cookies.set(
            name=cookie["name"],
            value=cookie["value"],
            domain=domain,
            path=cookie["path"]
        )


def visit_zoneh_after_login(page: Page):
    """
    Visiting that specific page after login so that we get the captcha to solve -
        and only this we take the cookies and insert them to the requests session -
            to be able to scrape the other pages FASTER.
    """

    page.goto(f"{BASE_URL}/archive")
    page.wait_for_load_state("networkidle")
