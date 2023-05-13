from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def create_driver():
    s = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--v=99")
    options.add_argument("--no-sandbox")
    options.add_argument(f"--user-data-dir=Cookies")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=s, chrome_options=options)
    return driver


def createDriver(headless=True, cookies=False):
    """
    start driver
    :return: driver
    """
    s = Service(ChromeDriverManager().install())
    # some options for deiver
    chrome_options = webdriver.ChromeOptions()
    if cookies:
        chrome_options.add_argument(f"--user-data-dir=Cookies")
    if headless:
        chrome_options.add_argument('--headless=new')  # headless or not

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--v=99")

    driver = webdriver.Chrome(service=s, chrome_options=chrome_options)
    driver.set_window_size(1920, 1080)
    return driver





# chrome_options.add_argument('window-size=1366x768')  # resolution
    # chrome_options.add_argument("--start-maximized")  # maximized or not
    # chrome_options.add_argument('--ignore-ssl-errors=yes')
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--allow-running-insecure-content')
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript': 2})
    # prefs = {"download.default_directory": MAIN_PATH, "safebrowsing.enabled": "false"}
    # chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")