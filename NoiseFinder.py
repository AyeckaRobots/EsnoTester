from EsnoGet import read_current_esno
from api_request import *
from JsonHandler import *


def print_noise_dict(distances):
    for key, value in dict.items(distances):         
        print(f"esno distance: {key}, on noise: {value}, hex: {hex(value)}")
        

def get_esno_pls(token, ip):
    esno = int(read_current_esno().split('(')[1][0:-1]) / 100
    
    psk, code = get_modcod(token, ip)
    return (esno, psk, code)


def evaluate_esno(token, ip):
    esno, psk, code = get_esno_pls(token, ip)
    
    exp_esno = float(read_esno_table(psk, code))
    print("#####################")
    print(f"modulation: {psk}\ncode: {code}")
    print(f"current esno: {esno}\nexp. esno: {exp_esno}")
    print("#####################")

    return round(esno - exp_esno, 2), esno, psk, code, exp_esno


def get_modcod(token, ip):
    signal_type = get_stats(token, ip)['signal_type']
    psk, code = (signal_type.split("_")[1] + "_" + signal_type.split("_")[2]).split("PSK")
    code = code.replace("_", "/")
    psk = psk + "PSK"
    return psk, code


def set_initial_noise(token, ip, psk, code):
    initial = read_initial_noise(psk, code)
    if not initial:
        return
    
    data = [{"address":24688, "value": initial}]
    
    print("setting noise to: ", data)
    update_noise(token, ip, data)


def adjustNoise(ip):
    username = "admin"
    password = "admin"
    expected_esno = 0

    token = get_auth(username, password, ip)

    if token == -1:
        print("No connection established. exiting program.")
        return
    
    update_modulator(token, ip)
    
    psk, code = get_modcod(token, ip)
    set_initial_noise(token, ip, psk, code)
    
    distance, current_esno, psk, code, expected_esno = evaluate_esno(token, ip)
    
    esno_multiplier_rate = max(0.5, min(3, abs(4 / expected_esno)))
    
    distances = {distance: get_current_noise(token, ip)}
    while abs(distance) > allowed_esno_error:
        print_noise_dict(distances)
        if  current_esno <= -10.00 or current_esno >= 40:  # if esno is outside of acceptable range. probobly didnt get measured correctly
            distance, current_esno, *_ = evaluate_esno(token, ip)
            print('bad esno: ', current_esno)
            continue
        # print(datetime.datetime())
            
        new_noise = int(max(min_noise, min(max_noise, distances[distance] + distance*error_multiplier*esno_multiplier_rate)))
        
        data = [{"address":24688, "value": new_noise}]
        update_noise(token, ip, data)
        
        distance, current_esno, psk, code, expected_esno = evaluate_esno(token, ip)   
    
        distances.update({distance: get_current_noise(token, ip)})
        
        
    print_noise_dict(distances)
    insert_initial_noise(psk, code, [*distances.values()][-1])
    


def main():

    ipaddress = input("Enter the ip of the device. (press enter for 192.168.15.10)")
    if ipaddress == '':
        ipaddress = "192.168.15.10"
    adjustNoise(ipaddress)


if __name__ == "__main__":
    max_noise = 115232  # 1c220
    min_noise = 114688  # 1c000
    allowed_esno_error = 0.1
    error_multiplier = 10
    main()
