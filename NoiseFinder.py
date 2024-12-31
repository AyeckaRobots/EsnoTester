# from time import sleep
# import datetime
# import json
# import time
import requests
from EsnoGet import read_current_esno
from DatabaseHandle import get_data_as_string, insert_db_initial_noise
from api_request import *


def print_noise_dict(distances):
    for key, value in dict.items(distances):         
        print(f"esno distance: {key}, on noise: {value}, hex: {hex(value)}")
        

def get_esno_pls(token, ip):
    esno = int(read_current_esno().split('(')[1][0:-1]) / 100
    
    signal_type = get_stats(token, ip)['signal_type']
    psk, code = (signal_type.split("_")[1] + "_" + signal_type.split("_")[2]).split("PSK")
    psk = psk + "PSK"
    code = code.replace("_", "/")
    return (esno, psk, code)


def evaluate_esno(token, ip):
    esno, psk, code = get_esno_pls(token, ip)
    
    exp_esno = float(get_data_as_string()[psk][code])
    print("#####################")
    print(f"modulation: {psk}\ncode: {code}")
    print(f"current esno: {esno}\nexp. esno: {exp_esno}")
    print("#####################")

    return round(esno - exp_esno, 2), esno, psk, code


def adjustNoise(ip):
    username = "admin"
    password = "admin"

    token = get_auth(username, password, ip)
    psk = ""
    code = ""
    # print(f"got token: {token}")

    if token == -1:
        print("No connection established. exiting program.")
        return
    
    update_modulator(token, ip)
    
    distance, current_esno, psk, code = evaluate_esno(token, ip)
    
    distances = {distance: get_current_noise(token, ip)}
    while abs(distance) > allowed_esno_error:
        if  current_esno <= -10.00 or current_esno >= 40:  # if esno is outside of acceptable range. probobly didnt get measured correctly
            distance, current_esno, *_ = evaluate_esno(token, ip)
            print('bad esno: ', current_esno)
            continue
        # print(datetime.datetime())
            
        new_noise = int(max(min_noise, min(max_noise, distances[distance] + distance*error_multiplier)))
        
        data = [{"address":24688, "value": new_noise}]
        update_noise(token, ip, data)
        
        distance, current_esno, psk, code = evaluate_esno(token, ip)   
    
        distances.update({distance: get_current_noise(token, ip)})
        
        print_noise_dict(distances)
        
        
    insert_db_initial_noise(psk, code, [*distances.values()][-1])
    


def main():

    ipaddress = input("Enter the ip of the device. (press enter for 192.168.15.10)")
    if ipaddress == '':
        ipaddress = "192.168.15.10"
    adjustNoise(ipaddress)


if __name__ == "__main__":
    max_noise = 115232  # 1c220
    min_noise = 114688  # 1c000
    allowed_esno_error = 0.1
    error_multiplier = 15
    main()
