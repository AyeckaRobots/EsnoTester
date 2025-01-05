import json
import os

from api_request import get_serial_number


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
    # print(pls)
    with open("pls_table.json") as file:
        pls_table = json.load(file)
        
        for modulation, codes in pls_table.items(): 
            for code, value in codes.items():
                if value == pls:
                    # print(f"found: {modulation}, {code}. Starting tests...")
                    return modulation, code
        print("couldnt find matching modcod to: ", pls)
  
        
def insert_result_dict(psk, code, missed_counter, sn):
    with open(f"SN{sn}.json", "r+") as jsonFile:
        data = json.load(jsonFile)

        if missed_counter > 0:
            data[psk][code] = "Failed"
        else:
            data[psk][code] = "Passed"


        jsonFile.seek(0)  # rewind
        json.dump(data, jsonFile, indent=4)
        jsonFile.truncate()


def create_result_dict(sn):
    if os.path.exists(f"SN{sn}.json"):
        return sn
    
    with open(f"SN{sn}.json", "x"):
        print(f"Created the test results file in the directory: SN{sn}.json")
    with open(f"SN{sn}.json", "r+") as jsonFile:
        data = {
    "QPSK": {
        "1/4": "",
        "1/3": "",
        "2/5": "",
        "1/2": "",
        "3/5": "",
        "2/3": "",
        "3/4": "",
        "4/5": "",
        "5/6": "",
        "8/9": "",
        "9/10": ""
    },
    "8PSK": {
        "3/5": "",
        "2/3": "",
        "3/4": "",
        "5/6": "",
        "8/9": "",
        "9/10": ""
    },
    "16APSK": {
        "2/3": "",
        "3/4": "",
        "4/5": "",
        "5/6": "",
        "8/9": "",
        "9/10": ""
    },
    "32APSK": {
        "3/4": "",
        "4/5": "",
        "5/6": "",
        "8/9": "",
        "9/10": ""
    }
}
        jsonFile.seek(0)  # rewind
        json.dump(data, jsonFile, indent=4)
        jsonFile.truncate()
