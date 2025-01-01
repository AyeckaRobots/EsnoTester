import json


def read_esno_dict(psk, code):
    with open('esno_table.json') as file:
        esno_dict = json.load(file)
        return esno_dict[psk][code]
    

def read_pls_dict():
    with open('pls_table.json') as file:
        pls_dict = json.load(file)
        return pls_dict
    
    
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
    
    
def get_modcod_from_pls(pls):
    with open("pls_table.json") as file:
        pls_table = json.load(file)
        
        for modulation, codes in pls_table.items():
            for code, value in codes.items():
                if value == pls:
                    return modulation, code
        print("couldnt find matching modcod to: ", pls)