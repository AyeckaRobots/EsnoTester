import json
import os

def read_esno_dict(pls):
    """Opens esno_table.json and returns value for specific modcod

    Args:
        psk (str): the modulation
        code (str): the code (error handling rate)

    Returns:
        int: the expected value for the modcod
    """
    with open('SystemUtils/PlsDict.json') as file:
        pls_dict = json.load(file)
        return pls_dict[f"{pls}"]['exp_esno']
    
    
def insert_initial_noise(pls, initial_noise):
    """Adds the given @initial_noise for a specific modcod to
    the initial_noise.json file

    Args:
        psk (str): the modulation
        code (str): the code
        initial_noise (int): the noise to start from for next time the modcod is tested
    """
    with open('SystemUtils/PlsDict.json', 'r+') as file:
        data = json.load(file)

        data[f"{pls}"]['initial_noise'] = initial_noise

        file.seek(0)  # rewind
        json.dump(data, file, indent=4)
        file.truncate()
        
        
def read_initial_noise(pls):
    """Reads the initial noise for a given modcod 

    Args:
        psk (str): the modulation
        code (str): the code

    Returns:
        int: the inital_noise for the given modcod
    """
    with open('SystemUtils/PlsDict.json') as file:
        pls_dict = json.load(file)
        return pls_dict[f"{pls}"]['initial_noise']

def initialize_result_dict(sn):
    import shutil
    shutil.copyfile("SystemUtils/PlsDict.json", f"TestResults/SN{sn}.json")
        
def insert_result_dict(pls, missed_counter, sn):
    """Adds a result (passed/failed for specific modcod) to the json file with corresponding name to
    the device's SN.

    Args:
        psk (str): the modulation
        code (str): the code
        missed_counter (int): amount of missed frames
        sn (int): the serial number of the device
    """

    if not os.path.exists(f"TestResults/SN{sn}.json"):
        initialize_result_dict(sn)

    with open(f"TestResults/SN{sn}.json", "r+") as jsonFile:
        data = json.load(jsonFile)

        if missed_counter > 0:
            data[f"{pls}"]['test_result'] = "Failed"
        else:
            data[f"{pls}"]['test_result'] = "Passed"


        jsonFile.seek(0)  # rewind
        json.dump(data, jsonFile, indent=4)
        jsonFile.truncate()

#
# def create_result_dict(sn):
#     """Creates a results file if it didn't already exist,
#       fills it with empty value for modcods
#
#     Args:
#         sn (int): the serial number if the device
#     """
#
#     if os.path.exists(f"SN{sn}.json"):
#         return
#
#     with open(f"SN{sn}.json", "x"):
#         print(f"Created the test results file in the directory: SN{sn}.json")
#     with open(f"SN{sn}.json", "r+") as jsonFile:
#         data = ""
#         with open("emptyModCod.json", 'r') as file:
#             data = json.load(file)
#
#         jsonFile.seek(0)  # rewind
#         json.dump(data, jsonFile, indent=4)
#         jsonFile.truncate()

def get_token_json(token_type):

    with open('SystemUtils/IpToken.json') as file:
        data = json.load(file)
        return data[f"{token_type}_token"]


def set_token_json(receiver_token, modulator_token):
    with open(f"SystemUtils/IpToken.json", "r+") as jsonFile:
        data = json.load(jsonFile)

        data['receiver_token'] = receiver_token
        data['modulator_token'] = modulator_token

        jsonFile.seek(0)  # rewind
        json.dump(data, jsonFile, indent=4)
        jsonFile.truncate()


def read_target_ip(target_type):
    # target type is: modulator, receiver
    with open(f"SystemUtils/IpToken.json") as jsonFile:

        data = json.load(jsonFile)
        return data[f"{target_type}_ip"]


def update_target_ip(target_type, new_ip):
    # target type is: modulator, receiver
    with open(f"SystemUtils/IpToken.json", "r+") as jsonFile:
        data = json.load(jsonFile)

        data[f"{target_type}_ip"] = new_ip

        jsonFile.seek(0)  # rewind
        json.dump(data, jsonFile, indent=4)
        jsonFile.truncate()