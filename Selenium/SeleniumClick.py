import time

from selenium.webdriver.common.action_chains import ActionChains

from Selenium.findElementByXpathToSelenium import search


def click(driver, xpathOrElement, debug=True, timer=2):
    try:
        if type(xpathOrElement).__name__ == "str":
            element = search(driver, xpathOrElement, debug=debug)
        else:
            element = xpathOrElement
        ActionChains(driver).move_to_element(element).click(element).perform()
        time.sleep(timer)
        return element
    except:
        return None
