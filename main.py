import requests
from bs4 import BeautifulSoup

URL = 'https://www.casasyterrenos.com/buscar/jalisco/zapopan/casas-y-departamentos/renta?page=4'
HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0 '
    }

if __name__ == '__main__':
    session = requests.session()
    response = session.get(URL, headers=HEADERS)

    if response.status_code == 200:
        content = response.text

        file_name = URL.split('/')[-1]

        with open(f'assets/templates/{file_name}.text', 'w+') as file:
            file.write(content)

            print('Tamplate generado con exito!')
    else:
        print(f'No se logro acceder al sitio! Respuesta del Server:{response.text}')

        
