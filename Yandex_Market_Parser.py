import pickle
import time
import traceback
import random

import Constants.MAIN_PARAMS
from Constants import MAIN_PARAMS, XPATHS
from Selenium import SeleniumClick, StartSelenium, ConnectToURL
from Selenium.findElementByXpathToSelenium import search


class YMP(object):
    def __init__(self):
        self.PAGES_COUNT = MAIN_PARAMS.PAGES
        # self.all_links = pickle.load(open("E://all_links.pkl", "rb"))
        self.all_links = []
        # self.characteristic = pickle.load(open("E://all_characteristic.pkl", "rb"))

    def start_selenium(self, headless=False, cookies=True):
        # self.driver = StartSelenium.createDriver(headless=headless, cookies=cookies)
        self.driver = StartSelenium.create_driver()
        try:
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
  '''
            })
            # print("links len: ", len(self.all_links))
            # print("charact len: ", len(self.characteristic.keys()))
            # self.characteristic = {}
            # self.go_every_link()
            self.go_to_main_page()
            # self.characteristic['1'] = [1,2,3]
            # print(self.characteristic)
        except:
            print(traceback.format_exc())
        finally:
            time.sleep(3)
            pickle.dump(self.all_links, open("E://all_links_YANDEX.pkl", "wb"))
            # pickle.dump(self.characteristic, open("E://all_characteristic.pkl", "wb"))
            self.driver.close()
            self.driver.quit()

    def go_to_main_page(self):
        # ConnectToURL.connect("https://market.yandex.ru/catalog--kvadrokoptery/18042097/list?srnum=1203&was_redir=1&rt=9&rs=eJwzCg1grGLl2L__K-ssRo4LWy42XNh3Ye8qRi6ODc0XeAWeX29nB3EOfWrngXNeAWk4B0XZOpgyAF4zJNE%2C&suggest=1&suggest_type=search&text=дрон&hid=12410815&how=dprice&allowCollapsing=1&local-offers-first=0&pricefrom=6000&priceto=150000&page=1", self.driver)
        # a = input()
        for page in range(Constants.MAIN_PARAMS.PAGES):
            url = f"https://market.yandex.ru/catalog--kvadrokoptery/18042097/list?srnum=1203&was_redir=1&rt=9&rs=" \
                  f"eJwzCg1grGLl2L__K-ssRo4LWy42XNh3Ye8qRi6ODc0XeAWeX29nB3EOfWrngXNeAWk4B0XZOpgyAF4zJNE%2C&suggest=" \
                  f"1&suggest_type=search&text=дрон&hid=12410815&how=dprice&allowCollapsing=1&local-offers-first=" \
                  f"0&pricefrom=6000&priceto=150000&page={page+1}"
            delay = random.randint(15, 30)
            ConnectToURL.connect(url, self.driver, delay=delay)
            self.bot_check()
            self.scroll_to_downside()
            self.find_all_links()
            # self.go_every_link()

    def find_all_links(self):
        all_titles_on_page = search(self.driver, "//h3/a", _list=True)
        print(len(all_titles_on_page))

        for headder in all_titles_on_page:
            # print(headder.get_attribute("href"))
            self.all_links.append(headder.get_attribute("href"))

    def go_every_link(self, stop_count=0):
        for index, link in enumerate(self.all_links):
            # print(index)
            if index + 1 < stop_count or stop_count == 0:
                if link not in self.characteristic.keys():
                    delay = random.randint(5, 10)
                    ConnectToURL.connect(link, self.driver, delay=delay)
                    # self.bot_check()
                    try:
                        keys = search(self.driver, "//div[@data-widget='paginator']//dl/dt", _list=True)
                        values = search(self.driver, "//div[@data-widget='paginator']//dl/dd", _list=True)
                        price = search(self.driver, "//div[@slot = 'content']//span/span", debug=False)
                        if price is None:
                            price = search(self.driver, "//span[@class = 'on4']/span")

                        _dict = {"price": price.text.replace("₽", "").replace(" ", "").replace('\u2009', "")}
                        for char_index in range(len(keys)):
                            try:
                                key = keys[char_index].text
                                value = values[char_index].text

                                _dict[key] = value
                            except:
                                print(traceback.format_exc())

                        print(index, _dict)
                        self.characteristic[link] = _dict
                    except:
                        print(traceback.format_exc())

    def scroll_to_downside(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def bot_check(self):
        element = search(self.driver, "//span[text() = 'Подтвердите, что запросы отправляли вы, а не робот']",
                         debug=False)
        while element is not None:
            print("Wait for captcha")
            time.sleep(1)
            element = search(self.driver, "//span[text() = 'Подтвердите, что запросы отправляли вы, а не робот']",
                             debug=False)
