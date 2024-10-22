#File with all the Config variables

class Config:

    TEST = True
    DOMAIN = 'https://www.casasyterrenos.com'
    HEADERS = {
        'Accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0 '
    }
    URL_PAGE = '/buscar/jalisco/zapopan/casas-y-departamentos/renta?page='
    PROPIERTIES_COLUMNS = ['Name', 'Price', 'Room', 'Bathroom', 'Toilet', 'Parking Lots', 'Description', 'Area']
