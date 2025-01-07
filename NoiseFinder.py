from EsnoGet import read_current_esno
from api_request import *
from JsonHandler import *

max_noise = 115232  # 1c220
min_noise = 114688  # 1c000
allowed_esno_error = 0.1
error_multiplier = 10

def print_noise_dict(distances):
    for key, value in dict.items(distances):         
        print(f"esno distance: {key}, on noise: {value}, hex: {hex(value)}")
        

def get_esno_pls(token, ip):
    esno = int(read_current_esno().split('(')[1][0:-1]) / 100
    
    psk, code = get_modcod(token, ip)
    return (esno, psk, code)


def evaluate_esno(token, ip):
    esno, psk, code = get_esno_pls(token, ip)
    
    exp_esno = float(read_esno_dict(psk, code))
    print("#####################")
    print(f"modulation: {psk}\ncode: {code}")
    print(f"current esno: {esno}\nexp. esno: {exp_esno}")
    print("#####################")

    return round(esno - exp_esno, 2), esno, psk, code, exp_esno


def get_modcod(token, ip):
    signal_pls_code = get_rx_status(token, ip)['test_pattern_pls_code']
    psk, code = get_modcod_from_pls(signal_pls_code)
    return psk, code


def set_initial_noise(token, ip, psk, code):
    initial = read_initial_noise(psk, code)
    if not initial:
        return
    
    data = [{"address":24688, "value": initial}]
    
    update_noise(token, ip, data)


def adjustNoise(token, ip):
    expected_esno = 0
    
    update_modulator(token, ip)
    
    psk, code = get_modcod(token, ip)
    set_initial_noise(token, ip, psk, code)
    
    distance, current_esno, psk, code, expected_esno = evaluate_esno(token, ip)
    try:
        esno_multiplier_rate = max(1, min(3, abs(4 / expected_esno)))
    except ZeroDivisionError as e:
        esno_multiplier_rate = 2
        
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
    return f"{psk} {code}"


def get_token(ipaddr):
    
    username = "admin"
    password = "admin"
    token = get_auth(username, password, ipaddr)
    
    if token == -1:
        print("No connection established. exiting program.")
        return
    
    return token


def main():

    ipaddress = input("Enter the ip of the device. (press enter for 192.168.15.10)")
    if ipaddr == '':
        ipaddr = "192.168.15.10"
        
    token = get_token()
    
    if token:
        adjustNoise(token, ipaddress)


if __name__ == "__main__":
    main()
