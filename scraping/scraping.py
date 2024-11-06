# File with the scraping class

import requests
import json

from config import Config
from bs4 import BeautifulSoup
from helpers import unwrap_json


LAYERS_TO_UNWRAP = [
    0,
    'props',
    'pageProps',
    'initialState',
    'propertyData',
    'properties'
    ]

headers = Config.HEADERS


class Scraping:
    """Father class that gets the content of a webpage using the URL given.
    """
    def __init__(self, url):
        """Constructor

        Args:
            url (string): URL of the web page to scrap.
        """
        self.url = url
        self._response_code = 0
        self._content = ""

    def _get_response(self):
        """Get the response obtained from the web request.

        Returns:
            integer: Response code
        """
        return self._response_code

    def _get_content(self):
        """Get the HTML content obtained from the web request.

        Returns:
            string: HTML code
        """
        return self._content

    def _get_web(self):
        """Send a request to the URL given and set up the response status code and the HTML content.

        Returns:
            string: HTML code
        """
        session = requests.session()
        response = session.get(self.url, headers=headers)

        # If the request was successful, get the HTML content. 
        # Else print an error message with the response status code.
        if response.status_code == 200:
            self._content = response.text
            self._response_code = response.status_code
            print('Se accedio correctamente')
        else:
            self._content = ""
            self._response_code = response.status_code
            print(f'No se logro acceder al sitio! Respuesta del Server:{response.status_code}')

        return self._content


class ScrapingPage(Scraping):
    """Class for scrap and add the URL of each property in a list.

    Args:
        Scraping (class): Father class
    """
    def __init__(self, url):
        """Constructor
        Args:
            url (string): URL of the web page to scrap.
        """
        self.url = url
        self._get_web()

    def get_properties(self):
        """Get a list of the URLs of each property.

        Returns:
            list: Strings of the URLs of each property
        """
        __url_properties = {}

        if self._get_response() == 200:
            soup = BeautifulSoup(self._get_content(), 'html.parser')

            # Extract a JSON from the HTML code with the URLs of all the properties.
            # This JSON is a nested dictionary. See the layers in LAYERS_TO_UNWRAP.
            properties_json = [json.loads(element.text) for element in soup.find_all('script', id='__NEXT_DATA__')]
            # Get only the URLs of all the properties from the JSON.
            properties_dirty = unwrap_json(properties_json, LAYERS_TO_UNWRAP)
            # Save the URLs in a clean list.
            __url_properties = [property['canonical'] for property in properties_dirty]

        return __url_properties


class ScrapingProperty(Scraping):
    """Class for scrap and add the items of each property to a list.

    Args:
        Scraping (class): Father class
    """
    def __init__(self, url):
        """Constructor

        Args:
            url (string): URL of the web page to scrap.
        """
        self.url = url
        self._soup = 0
        self._get_web()

    def get_items(self):
        """Get a list of the items of each property.

        Returns:
            list: Strings of the description of each item
        """
        __property_items = []

        if self._get_response() == 200:
            self._soup = BeautifulSoup(self._get_content(), 'html.parser')

            __property_items = [
                self._get_name(),
                self._get_price(),
                self._get_room(),
                self._get_bathroom(),
                self._get_toilet(),
                self._get_parking_lot(),
                self._get_description(),
                self._get_area()
                ]

        return __property_items

    def _get_name(self):
        """Get the property's name.

        Returns:
            string: property's name
        """
        __name = self._soup.find('h1', class_='font-bold text-gray-700 capitalize text-lg md:text-xl')

        return __name.text if __name else ""

    def _get_price(self):
        """Get the property's price.

        Returns:
             string: property's price
        """
        __price = self._soup.find('p', class_='text-2xl m-0')

        return __price.text if __price else ""

    def _get_room(self):
        """Get the number of rooms.

        Returns:
             string: number of rooms
        """
        __room = self._soup.find('img', src='/static/img/property_description/rooms.svg')

        return __room.next_sibling.text if __room else ""

    def _get_bathroom(self):
        """Get the number of bathrooms.

        Returns:
             string: number of bathrooms
        """
        __bathroom = self._soup.find('img', src='/static/img/property_description/bathrooms.svg')

        return __bathroom.next_sibling.text if __bathroom else ""

    def _get_toilet(self):
        """Get the number of toilets.

        Returns:
             string: number of toilets
        """
        __toilet = self._soup.find('img', src='/static/img/property_description/halfBathrooms.svg')

        return __toilet.next_sibling.text if __toilet else ""

    def _get_parking_lot(self):
        """Get the number of parking spaces.

        Returns:
             string: number of parking spaces
        """
        __parcking_lot = self._soup.find('img', src='/static/img/property_description/parking_lots.svg')

        return __parcking_lot.next_sibling.text if __parcking_lot else ""

    def _get_description(self):
        """Get the description of the property.

        Returns:
            string: description of the property
        """
        __description = self._soup.find('div', class_='prose max-w-screen-md')

        return [element.text for element in __description.children] if __description else ""

    def _get_area(self):
        """Get the area of the property.

        Returns:
            string: area of the property
        """
        __area = self._soup.find('p', class_='mb-0')

        return __area.text if __area else ""
