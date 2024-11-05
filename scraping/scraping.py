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
    def __init__(self, url):
        self.url = url
        self._response_code = 0
        self._content = ""

    def _get_response(self):
        return self._response_code

    def _get_content(self):
        return self._content

    def _get_web(self):
        session = requests.session()
        response = session.get(self.url, headers=headers)

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
    def __init__(self, url):
        self.url = url
        self._get_web()

    def get_properties(self):
        __url_properties = {}

        if self._get_response() == 200:
            soup = BeautifulSoup(self._get_content(), 'html.parser')

            properties_json = [json.loads(element.text) for element in soup.find_all('script', id='__NEXT_DATA__')]
            properties_dirty = unwrap_json(properties_json, LAYERS_TO_UNWRAP)
            __url_properties = [property['canonical'] for property in properties_dirty]

        return __url_properties


class ScrapingProperty(Scraping):
    def __init__(self, url):
        self.url = url
        self._soup = 0
        self._get_web()

    def get_items(self):
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
        __name = self._soup.find('h1', class_='font-bold text-gray-700 capitalize text-lg md:text-xl')

        return __name.text if __name else ""

    def _get_price(self):
        __price = self._soup.find('p', class_='text-2xl m-0')

        return __price.text if __price else ""

    def _get_room(self):
        __room = self._soup.find('img', src='/static/img/property_description/rooms.svg')

        return __room.next_sibling.text if __room else ""

    def _get_bathroom(self):
        __bathroom = self._soup.find('img', src='/static/img/property_description/bathrooms.svg')

        return __bathroom.next_sibling.text if __bathroom else ""

    def _get_toilet(self):
        __toilet = self._soup.find('img', src='/static/img/property_description/halfBathrooms.svg')

        return __toilet.next_sibling.text if __toilet else ""

    def _get_parking_lot(self):
        __parcking_lot = self._soup.find('img', src='/static/img/property_description/parking_lots.svg')

        return __parcking_lot.next_sibling.text if __parcking_lot else ""

    def _get_description(self):
        __description = self._soup.find('div', class_='prose max-w-screen-md')

        return [element.text for element in __description.children] if __description else ""

    def _get_area(self):
        __area = self._soup.find('p', class_='mb-0')

        return __area.text if __area else ""
