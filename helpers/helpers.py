#File with general functions

import pandas as pd

from config import Config

properties_columns = Config.PROPIERTIES_COLUMNS

def unwrap_json(objson: dict, layers: list):
    """Return an unwrap json"""
    new_json = objson[layers[0]] #Unwrap the original JSON
    layers.pop(0) #Delete the first Layer
    return new_json if not layers else unwrap_json(new_json, layers) #If there aren´t layers return JSON else keep unwrapping


def convert_to_csv(properties_dic):
    """Convert a dictionary to a csv file"""
    df = pd.DataFrame(properties_dic, columns=properties_columns)

    print("Original DataFrame:")
    print(df)
    print('Data from properties.csv:')

    df.to_csv('assets/properties.csv', header=True)    
