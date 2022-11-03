from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager


def create() -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "download": {
            "prompt_for_download": False,
            "directory_upgrade": True,
            "default_directory": '/tmp/data'
        },
    }
    chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    return webdriver.Remote("http://chrome:4444/wd/hub", options=chrome_options)
