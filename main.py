import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

DOMAIN = 'https://www.casasyterrenos.com'
URL = '/buscar/jalisco/zapopan/casas-y-departamentos/renta?page=1'
HEADERS = {
        'Accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0 '
    }
LAYERS_TO_UNWRAP = [0, 'props', 'pageProps', 'initialState', 'propertyData', 'properties']

properties_columns = ['Name', 'Price', 'Room', 'Bathroom', 'Parking Lots', 'Description', 'Area']
properties_dic = {
    'Name': [],
    'Price': [],
    'Room': [],
    'Bathroom': [],
    #'Toilet': [],
    'Parking Lots': [],
    'Description': [],
    'Area': []
}
bandera_chigona = 0

def unwrap_json(objson: dict, layers: list):
    new_json = objson[layers[0]] #Unwrap the original JSON
    layers.pop(0) #Delete the first Layer
    return new_json if not layers else unwrap_json(new_json, layers) #If there aren´t layers return JSON else keep unwrapping

if __name__ == '__main__':
    session = requests.session()
    response = session.get(DOMAIN + URL, headers=HEADERS)

    if response.status_code == 200:
        content = response.text

        page_name = URL.split('/')[-1]

        #with open(f'assets/templates/{page_name}.text', 'w+') as file:
        #    file.write(content)

        #    print('Tamplate generado con exito!')

        soup = BeautifulSoup(content, 'html.parser')

        properties_json = [json.loads(element.text) for element in soup.find_all('script', id='__NEXT_DATA__')]
        
        properties = unwrap_json(properties_json, LAYERS_TO_UNWRAP)
        
        for property in properties:
            url_property = property['canonical']
            response_property = session.get(DOMAIN + url_property, headers=HEADERS)
            
            if response_property.status_code == 200:
                content = response_property.text
                url_property = url_property.split('/')[-1]

                #with open(f'assets/templates/{url_property}.text', 'w+') as file:
                #    file.write(content)

                #    print('Tamplate generado con exito!')

                soup = BeautifulSoup(content, 'html.parser')

                properties_dic['Name'].append(soup.find('h1', class_='font-bold text-gray-700 capitalize text-lg md:text-xl').text)
                properties_dic['Price'].append(soup.find('p', class_='text-2xl m-0').text)
                properties_dic['Room'].append(soup.find('img', src='/static/img/property_description/rooms.svg').next_sibling.text) #Validar que si exista img con ese src
                properties_dic['Bathroom'].append(soup.find('img', src='/static/img/property_description/bathrooms.svg').next_sibling.text) #Validar que si exista img con ese src
                #properties_dic['Toilet'].append(soup.find('img', src='/static/img/property_description/halfBathrooms.svg').next_sibling.text) #Validar que si exista img con ese src
                properties_dic['Parking Lots'].append(soup.find('img', src='/static/img/property_description/parking_lots.svg').next_sibling.text) #Validar que si exista img con ese src
                properties_dic['Description'].append([element.text for element in soup.find('div', class_='prose max-w-screen-md').children]) #Validar que si exista img con ese src
                properties_dic['Area'].append(soup.find('p', class_='mb-0').text)

                if bandera_chigona == 5:

                    break

                bandera_chigona = bandera_chigona + 1

            else:
                print(f'No se logro acceder al sitio! Respuesta del Server:{response_property}')       
        
        df = pd.DataFrame(properties_dic, columns=properties_columns)

        print("Original DataFrame:")
        print(df)
        print('Data from Users.csv:')

        df.to_csv('assets/properties.csv', header=True)

    else:
        print(f'No se logro acceder al sitio! Respuesta del Server:{response.text}')

        
