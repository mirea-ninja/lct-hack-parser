from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

DOWNLOAD_DIR = str(Path.cwd())


def create() -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("prefs", {"download.default_directory": DOWNLOAD_DIR})

    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"  # interactive
    return webdriver.Chrome(
        ChromeDriverManager().install(),
        options=chrome_options,
        desired_capabilities=caps,
    )
