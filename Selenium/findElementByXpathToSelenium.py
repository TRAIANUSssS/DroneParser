from selenium.webdriver.common.by import By

def search(driver, xpath, _list=False, debug=True):
    try:
        if _list == False:
            return driver.find_element(By.XPATH, f"{xpath}")
        else:
            return driver.find_elements(By.XPATH, f"{xpath}")
    except:
        if debug:
            print(xpath)
            print('find error')
        return None
