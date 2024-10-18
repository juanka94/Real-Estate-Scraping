import requests
import json
from bs4 import BeautifulSoup

DOMAIN = 'https://www.casasyterrenos.com'
URL = '/buscar/jalisco/zapopan/casas-y-departamentos/renta?page=4'
HEADERS = {
        'Accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0 '
    }
LAYERS_TO_UNWRAP = [0, 'props', 'pageProps', 'initialState', 'propertyData', 'properties']

def unwrap_json(objson: dict, layers: list):
    new_json = objson[layers[0]] #Unwrap the original JSON
    layers.pop(0) #Delete the first Layer
    return new_json if not layers else unwrap_json(new_json, layers) #If there aren´t layers return JSON else keep unwrapping

if __name__ == '__main__':
    session = requests.session()
    response = session.get(DOMAIN + URL, headers=HEADERS)

    if response.status_code == 200:
        content = response.text

        file_name = URL.split('/')[-1]

        with open(f'assets/templates/{file_name}.text', 'w+') as file:
            file.write(content)

            print('Tamplate generado con exito!')

        soup = BeautifulSoup(content, 'html.parser')

        properties_json = [json.loads(element.text) for element in soup.find_all('script', id='__NEXT_DATA__')]
        
        properties = unwrap_json(properties_json, LAYERS_TO_UNWRAP)

        for property in properties:
            url_property = property['canonical']
            response_property = session.get(DOMAIN + url_property, headers=HEADERS)

            if response.status_code == 200:
                content = response.text

                print('Tamplate generado con exito!')
            else:
                print(f'No se logro acceder al sitio! Respuesta del Server:{response.status_code}')
            

            
    else:
        print(f'No se logro acceder al sitio! Respuesta del Server:{response.text}')

        
