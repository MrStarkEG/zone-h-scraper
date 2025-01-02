# import os

class BrowserHandler:
    """A class to handle browser operations using Playwright."""

    def __init__(self, headless: bool = True):
        """
        Initializes the browser handler.

        :param headless: Boolean indicating if the browser should run in headless mode.
        """
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

    def get_random_user_agent(self) -> str:
        """Returns a random user-agent from the list."""
        # return random.choice(self.user_agent_list)
        pass

    def launch_browser(self, playwright, cookies):
        """Launches the browser, creates a context and page."""
        # user_agent = self.get_random_user_agent()
        # data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        # data_dir_chrome = os.path.join(data_dir, "data_dir")
        self.browser = playwright.chromium.launch(
            headless=self.headless,
            args=["--no-sandbox"],
            # user_data_dir= data_dir_chrome
        )

        self.context = self.browser.new_context(
            user_agent=self.USER_AGENT,
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate",
            },
            ignore_https_errors=True,
        )

        self.context.add_cookies(cookies)
        # self.context = self.browser.new_context()
        self.page = self.context.new_page()

        return self.page

    def close_browser(self):
        """Closes the browser and cleans up resources."""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
