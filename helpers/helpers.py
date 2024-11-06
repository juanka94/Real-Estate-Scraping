# File with general functions

import pandas as pd

from config import Config

properties_columns = Config.PROPIERTIES_COLUMNS


def unwrap_json(objson: dict, layers: list):
    """Remove the layers of a nested JSON.

    Args:
        objson (dict): Nested JSON
        layers (list): Layers to remove

    Returns:
        dict: Unnested
    """
    new_json = objson[layers[0]]  # Unwrap the original JSON
    layers.pop(0)  # Delete the first Layer
    # If there aren´t layers return JSON else keep unwrapping
    return new_json if not layers else unwrap_json(new_json, layers)


def convert_to_csv(properties_dic):
    """Convert a dictionary to a csv file"""
    df = pd.DataFrame(properties_dic, columns=properties_columns)

    df.to_csv('assets/properties.csv', header=True)
