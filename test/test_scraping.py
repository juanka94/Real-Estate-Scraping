import pytest

from scraping import ScrapingPage, ScrapingProperty

URL_PAGE = "https://www.casasyterrenos.com/buscar/jalisco/zapopan/casas-y-departamentos/renta?page=1"
URL_PROPERTY = "https://www.casasyterrenos.com/propiedad/departamento-renta-puesta-del-sol-lomas-altas-zapopan-jal-3718620"

@pytest.fixture
def empty_scraping_page():
    return ScrapingPage(URL_PAGE)


@pytest.fixture
def empty_scraping_property():
    return ScrapingProperty(URL_PROPERTY)


def test_get_properties(empty_scraping_page):
    properties = empty_scraping_page.get_properties()

    assert len(properties) == 40

def test_get_items(empty_scraping_property):
    items = empty_scraping_property.get_items()

    assert len(items) == 8