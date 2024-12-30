from time import sleep

import json
import requests
from EsnoSetter import read_current_esno
from DatabaseHandle import get_data_as_string

def get_auth(username, password, ip):
    try:
        response = requests.post(f"http://{ip}/api/login", json={"username": username, "password": password})
    except TimeoutError as e:
        print(f"couldn't connect to ip: {ip} ")
        return -1
    print(response.json())
    return f"Bearer {response.json()['token']}"


def get_advanced_stats(token, ip):
    try:
        data = requests.get(f"http://{ip}/api/advanced_status", headers={'Authorization': token})
    except TimeoutError as e:
        print(f"No response from {ip}, error: {e}")
        return -1

    return data.json()["agg_slices"][1]


def read_esno():

    # Open and read the JSON file
    with open("esno.json", 'r') as file:
        data = json.load(file)

    print(data)


def changeNoise(ip):
    username = "admin"
    password = "admin"

    token = get_auth(username, password, ip)
    print(f"got token: {token}")

    if token == -1:
        print("No connection established. exiting program.")
        return
    
    data = {"enable":True,"frequency":1200000,"symbol_rate":12000,
            "power":-30,"roll_off":"Alpha_020","spectral_inversion":False,
            "gold_code":0,"carrier_mode":"CM_MODULATED","power_up_state":"On",
            "acm_mode":"AcmModeOff","buc_power":False,"buc_10MHz_output":False}
    response = requests.post(f"http://{ip}/api/modulator", headers={'Authorization': token}, json=data)	
    
    #send debug-write
    data = [{"address":24688,"value":114816}]
    response = requests.post(f"http://{ip}/api/fpga_write", headers={'Authorization': token}, json=data)


def main():

    ipaddress = input("Enter the ip of the device. (just press enter for 192.168.15.10)")
    if ipaddress == '':
        ipaddress = "192.168.15.10"
    changeNoise(ipaddress)


if __name__ == "__main__":
    main()