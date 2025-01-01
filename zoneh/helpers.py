import os
from datetime import datetime
from playwright.sync_api import Page
from anticaptchaofficial.imagecaptcha import *
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from config import ANTICAPTCHA_KEY


def convert_to_iso_format(time_str):
    """
    Checking if the time string is in the format of "YYYY/MM/DD" or "HH:MM" or "HH:MM:SS"
    and converting it to ISO format.

    Args:
        time_str (str): The time string to be converted.

    Returns:
        str: The time string in ISO format (for the ease of search of ElasticSearch).
    """
    try:
        date_obj = datetime.strptime(time_str, "%Y/%m/%d")
        return date_obj.isoformat()
    except ValueError:

        try:
            today = datetime.today()

            if len(time_str.split(":")) == 3:
                time_obj = datetime.strptime(time_str, "%H:%M:%S")
            else:

                time_obj = datetime.strptime(time_str, "%H:%M")

            adjusted_datetime = datetime.combine(today.date(), time_obj.time())

            return adjusted_datetime.isoformat()

        except ValueError:
            return "Invalid date or time format"


def get_captcha_screenshot(page):
    """
    Get the captcha screenshot of the captcha element and save it to a file
        to be solved by solve_captcha_screenshot function.
    """

    captcha_element = page.locator('img[id="cryptogram"]')
    captcha_element.screenshot(path="captcha.jpeg")

    return os.path.abspath("captcha.jpeg")


def solve_captcha_screenshot(img_path):
    """
    Solve the captcha screenshot using the anticaptcha API.
    """

    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(ANTICAPTCHA_KEY)
    solver.set_soft_id(0)

    captcha_text = solver.solve_and_return_solution(img_path)
    if captcha_text != 0:
        print("captcha text solved: " + captcha_text)
    else:
        print("task finished with error " + solver.error_code)

    return captcha_text


def delete_captcha_screenshot():
    """
    Delete the captcha screenshot to clean up.
    """

    if os.path.exists("captcha.jpeg"):
        os.remove("captcha.jpeg")
        print("Deleted captcha image.")
    else:
        print("The captcha image does not exist.")


@retry(
    stop=stop_after_attempt(5),
    wait=wait_fixed(7),
    retry=retry_if_exception_type(Exception),
)
def solve_captcha_with_playwright_return_cookies(page: Page):
    """
    Making sure that we solve the captcha and return the cookies after solving it.
    Also using the tenacity in case that the provider is down.
    """

    while '<img id="cryptogram" src="/captcha.py">' in page.content():
        captcha_img_path = get_captcha_screenshot(page)
        captcha_text = solve_captcha_screenshot(captcha_img_path)
        delete_captcha_screenshot()

        page.fill('//*[@id="propdeface"]/form/input[1]', captcha_text)
        page.click('//*[@id="propdeface"]/form/input[2]')

        page.wait_for_load_state("networkidle")

    return page.context.cookies()


def save_to_jsonl_file(data, filename: str = 'data.jsonl'):
    """
    Save the data to a JSONL file.

    Args:
        data (json data): The data to be saved.
        filename (str): The filename to save the data to.
    """

    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    data_folder = os.path.join(parent_directory, 'data')

    os.makedirs(data_folder, exist_ok=True)

    file_path = os.path.join(data_folder, filename)

    with open(file_path, "a", encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")
