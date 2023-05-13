import time

import requests

def connect(URL, driver=None, delay=5, _print = True):
    """
    Connecting to site
    :param URL:  url
    :param driver: if you need to connect a driver, then specify it in the parameters, otherwise specify only the url
    :return: driver or request
    """
    if driver is None:
        r = requests.get(URL)  # req to site
        if r.status_code != 200:  # if isn't ok
            print(f"Connection error. Status code: {r.status_code}")
            return None
        return r
    else:
        driver.get(URL)  # connect driver to the site
        print(f'Wait {delay} sec') if _print else None
        time.sleep(delay)
