import json


def save_dict_to_json(dict_object, filename):
    with open(filename, 'w') as file:
        json.dump(dict_object, file, indent=4)


def load_dict_from_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)
