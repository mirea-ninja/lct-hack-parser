import os.path

from selenium import webdriver


def create(unique_folder_name: str) -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    default_directory = str(os.path.join("/tmp/data", unique_folder_name))
    prefs = {
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.images": 2,
        "download": {
            "prompt_for_download": False,
            "directory_upgrade": True,
            "default_directory": default_directory,
        },
    }
    chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    return webdriver.Remote("http://chrome:4444/wd/hub", options=chrome_options)
