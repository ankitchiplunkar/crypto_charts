import json


def get_abi(contract):
    with open(f'../abi/{contract}.json') as json_file:
        return json.load(json_file)
