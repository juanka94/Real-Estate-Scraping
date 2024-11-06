# This file contains the main code to run the Real State Scraping.

from config import Config
from scraping import ScrapingPage, ScrapingProperty
from helpers import convert_to_csv
from threading import Thread

# Set up the variables with the URLs from the config file.
domain = Config.DOMAIN
base_url_page = Config.URL_PAGE
# List of the items of a property.
properties_columns = Config.PROPIERTIES_COLUMNS
# TODO: Create a test environment.
test = Config.TEST

# Structure of the dictionary
# where the items of the properties are going to be stored.
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
    """With the URL of a property, get all its items and save it in properties_dic.

    Args:
        url (string): URL of a propery
    """
    property_url = domain + url

    scraping_property = ScrapingProperty(property_url)
    items_property = scraping_property.get_items()

    for (item, column) in zip(items_property, properties_columns):
        properties_dic[column].append(item)


if __name__ == '__main__':
    # Set up the URL where the properties are.
    #  TODO: Add the possibility of scraping more than 1 page.
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
