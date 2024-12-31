import json


def read_esno_table(psk, code):
    with open('esno_table.json') as file:
        esno_table = json.load(file)
        return esno_table[psk][code]
    
    
def insert_initial_noise(psk, code, initial_noise):
    with open("initial_noise.json", "r+") as jsonFile:
        data = json.load(jsonFile)

        data[psk][code] = initial_noise

        jsonFile.seek(0)  # rewind
        json.dump(data, jsonFile, indent=4)
        jsonFile.truncate()
        
        
def read_initial_noise(psk, code):
    with open('initial_noise.json') as file:
        esno_table = json.load(file)
        return esno_table[psk][code]
    