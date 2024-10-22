#File with general functions

def unwrap_json(objson: dict, layers: list):
    """Return an unwrap json"""
    new_json = objson[layers[0]] #Unwrap the original JSON
    layers.pop(0) #Delete the first Layer
    return new_json if not layers else unwrap_json(new_json, layers) #If there aren´t layers return JSON else keep unwrapping
