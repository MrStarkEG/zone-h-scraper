import requests
from playwright.sync_api import sync_playwright
from browser import BrowserHandler

from scrapers import (scrape_onold_section,
                      scrape_archive_section,
                      scrape_archive_star_section)
from utils import (convert_cookies,
                   visit_zoneh_after_login,
                   add_playwright_cookies_to_requests)
from login import login_to_zoneh_using_requests
from helpers import solve_captcha_with_playwright_return_cookies


session = requests.Session()

if __name__ == "__main__":

    returned_cookies = login_to_zoneh_using_requests(session)

    with sync_playwright() as playwright:
        page = BrowserHandler().launch_browser(
            playwright, convert_cookies(returned_cookies))

        # browser = playwright.chromium.launch(headless=False)

        # context = browser.new_context()
        # page = browser.new_page()

        visit_zoneh_after_login(page)

        cookies_after_captcha = solve_captcha_with_playwright_return_cookies(
            page)

        add_playwright_cookies_to_requests(session, cookies_after_captcha)
        page.close_browser()

        # The magic happens here
        scrape_archive_section(session)
        scrape_archive_star_section(session)
        scrape_onold_section(session)
