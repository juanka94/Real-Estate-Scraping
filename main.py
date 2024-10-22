import pandas as pd

from config import Config
from scraping import ScrapingPage, ScrapingProperty

domain = Config.DOMAIN
url_page = Config.URL_PAGE

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

if __name__ == '__main__':

    scraping_page = ScrapingPage(domain+url_page)
    url_properties = scraping_page.get_properties()

    scraping_property = ScrapingProperty(domain+url_properties[0])
    properties_dic = scraping_property.get_items()

    print(properties_dic)
    

def convert_to_csv():
    df = pd.DataFrame(properties_dic, columns=properties_columns)

    print("Original DataFrame:")
    print(df)
    print('Data from Users.csv:')

    df.to_csv('assets/properties.csv', header=True)        
