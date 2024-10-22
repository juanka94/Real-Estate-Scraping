import pandas as pd

from config import Config
from scraping import ScrapingPage, ScrapingProperty
from helpers import convert_to_csv
from threading import Thread

domain = Config.DOMAIN
base_url_page = Config.URL_PAGE
properties_columns = Config.PROPIERTIES_COLUMNS
test = Config.TEST

properties_dic = {
    'Name': [],
    'Price': [],
    'Room': [],
    'Bathroom': [],
    'Toilet': [],
    'Parking Lots': [],
    'Description': [],
    'Area': []
}
threads = []

def get_property_items(url):
    property_url = domain + url

    scraping_property = ScrapingProperty(property_url)
    items_property = scraping_property.get_items()

    for (item, column) in zip(items_property, properties_columns):
        properties_dic[column].append(item)

if __name__ == '__main__':

    page_url = domain + base_url_page

    scraping_page = ScrapingPage(page_url)
    url_properties = scraping_page.get_properties()

    for url_property in url_properties:
        t = Thread(target=get_property_items(url_property))
        t.start()

        threads.append(t)

    for t in threads:
        t.join()

    convert_to_csv(properties_dic)
