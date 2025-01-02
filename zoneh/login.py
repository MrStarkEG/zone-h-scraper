import requests
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from config import USERNAME, PASSWORD
from utils import get_existing_cookies
from schemas import LoginFailedException


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(5),
    retry=retry_if_exception_type(LoginFailedException),
)
def login_to_zoneh_using_requests(session, username: str = USERNAME, password: str = PASSWORD):
    """
    Login to Zone-H using requests and return the cookies.

    Args:
    -----
        session (requests.Session): The existing requests session.
        username (str): The username to login with.
        password (str): The password to login with.

    Returns:
    --------
        dict: The cookies in requests format.
    """
    url = "https://www.zone-h.org/login"

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": get_existing_cookies(),
        "referer": "https://www.zone-h.org/login",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    credentials = {
        "login": username,
        "password": password
    }

    response = session.post(url, headers=headers, data=credentials)

    # print(credentials)

    if response.status_code == 200 and "Logout" in response.text:
        print("Login successful")
        return session.cookies.get_dict()
    else:
        raise LoginFailedException("Login failed")
