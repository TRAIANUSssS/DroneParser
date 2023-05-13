import pickle
import time
import traceback

from Selenium import StartSelenium, ConnectToURL
from Selenium.findElementByXpathToSelenium import search


class RC_Today(object):
    def __init__(self):
        self.characteristic = {}
        self.all_links = []
        # self.all_links = pickle.load(open("all_links_RS_STODAT_v3.pkl", "rb"))
        # self.characteristic = pickle.load(open("all_characteristic_RS_STODAT_v2.pkl", "rb"))

    def start_selenium(self, headless=False, cookies=True):
        self.driver = StartSelenium.create_driver()
        try:
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                'source': '''
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
          '''
            })
            print("links len: ", len(self.all_links))
            print("charact len: ", len(self.characteristic.keys()))

            self.go_to_main_page()
            self.go_every_link()
        except:
            print(traceback.format_exc())
        finally:
            time.sleep(3)
            pickle.dump(self.all_links, open("E://all_links_RS_STODAT_v3.pkl", "wb"))
            pickle.dump(self.characteristic, open("E://all_characteristic_RS_STODAT_v2.pkl", "wb"))
            self.driver.close()
            self.driver.quit()

    def go_to_main_page(self):
        ConnectToURL.connect("https://rc-today.ru/kvadrokoptery/?v[price1]=150000&v[price2]=1666700&p=ALL", self.driver)
        self.find_all_links()

    def find_all_links(self):
        all_titles_on_page = search(self.driver, "//a[@class = 'product_item__name__link']", _list=True)
        print(len(all_titles_on_page))

        for headder in all_titles_on_page:
            self.all_links.append(headder.get_attribute("href"))

    def go_every_link(self):
        for index, link in enumerate(self.all_links):
            if link not in self.characteristic.keys():
                ConnectToURL.connect(link, self.driver)
                try:
                    description = search(self.driver, "//div[@itemprop = 'description']").text
                    price = search(self.driver, "//div[@class = 'product_page__buttons']//span")
                    price = price.text.replace("руб.", "").replace(" ", "").strip()
                    keys = search(self.driver, "//tr/td[1]", _list=True)
                    values = search(self.driver, "//tr/td[2]", _list=True)

                    info_dict = {}
                    for key_index in range(len(keys)):
                        info_dict[keys[key_index].text] = values[key_index].text

                    self.characteristic[link] = [price, info_dict, description]

                    print(index, [price, info_dict, description])
                except:
                    print(traceback.format_exc())
            else:
                print(index, "link already parsed")

