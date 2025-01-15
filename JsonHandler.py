import json
import os
from Sm1xTester import STANDARD_USE

def read_esno_dict(psk, code, standard=STANDARD_USE):
    """Opens esno_table.json and returns value for specific modcod

    Args:
        psk (str): the modulation
        code (str): the code (error handling rate)

    Returns:
        int: the expected value for the modcod
    """
    with open('esno_table.json') as file:
        esno_dict = json.load(file)
        return esno_dict[standard ][psk][code]
    

def read_pls_dict():
    """Opens pls_table.json and returns it whole

    Returns:
        dict: the pls for each modcod
    """
    with open('pls_table.json') as file:
        pls_dict = json.load(file)
        return pls_dict
    
    
def insert_initial_noise(psk, code, initial_noise, standard=STANDARD_USE):
    """Adds the given @initial_noise for a specific modcod to
    the initial_noise.json file

    Args:
        psk (str): the modulation
        code (str): the code
        initial_noise (int): the noise to start from for next time the modcod is tested
    """
    with open("initial_noise.json", "r+") as jsonFile:
        data = json.load(jsonFile)

        data[standard][psk][code] = initial_noise

        jsonFile.seek(0)  # rewind
        json.dump(data, jsonFile, indent=4)
        jsonFile.truncate()
        
        
def read_initial_noise(psk, code, standard=STANDARD_USE):
    """Reads the initial noise for a given modcod 

    Args:
        psk (str): the modulation
        code (str): the code

    Returns:
        int: the inital_noise for the given modcod
    """
    with open('initial_noise.json') as file:
        esno_table = json.load(file)
        return esno_table[standard][psk][code]
    
    
def get_modcod_from_pls(pls, standard=STANDARD_USE):
    """A function to convert pls to modcod

    Args:
        pls (int): the pls to convert

    Returns:
        succses:    tuple: modulation and code (both string)
        fail:   str: no match for pls requested
    """
    with open("pls_table.json") as file:
        pls_table = json.load(file)
        
        for modulation, codes in pls_table[standard].items():
            for code, value in codes.items():
                if value == pls:
                    return modulation, code
        print("couldnt find matching modcod to: ", pls)
  
        
def insert_result_dict(psk, code, missed_counter, sn, standard=STANDARD_USE):
    """Adds a result (passed/failed for specific modcod) to the json file with corresponding name to
    the device's SN.

    Args:
        psk (str): the modulation
        code (str): the code
        missed_counter (int): amount of missed frames
        sn (int): the serial number of the device
    """
    with open(f"SN{sn}.json", "r+") as jsonFile:
        data = json.load(jsonFile)

        if missed_counter > 0:
            data[standard][psk][code] = "Failed"
        else:
            data[standard][psk][code] = "Passed"


        jsonFile.seek(0)  # rewind
        json.dump(data, jsonFile, indent=4)
        jsonFile.truncate()


def create_result_dict(sn):
    """Creates a results file if it didn't already exist,
      fills it with empty value for modcods

    Args:
        sn (int): the serial number if the device
    """
    
    if os.path.exists(f"SN{sn}.json"):
        return
    
    with open(f"SN{sn}.json", "x"):
        print(f"Created the test results file in the directory: SN{sn}.json")
    with open(f"SN{sn}.json", "r+") as jsonFile:
        data = ""
        with open("emptyModCod.json", 'r') as file:
            data = json.load(file)

        jsonFile.seek(0)  # rewind
        json.dump(data, jsonFile, indent=4)
        jsonFile.truncate()
