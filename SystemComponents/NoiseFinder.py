from SystemUtils import StaticVars
from SystemUtils.EsnoGet import read_current_esno
from ApiRequest import *
from JsonHandler import *

max_noise = 115232  # 1c220
min_noise = 114688  # 1c000
allowed_esno_error = StaticVars.esno_acceptable
error_multiplier = 10

def print_noise_dict(distances):
    for key, value in dict.items(distances):         
        print(f"esno distance: {key}, on noise: {value}, hex: {hex(value)}")
        

def get_esno_pls(token, ip):
    esno = int(read_current_esno().split('(')[1][0:-1]) / 100
    
    pls = get_modcod(token, ip)
    return (esno, pls)


def evaluate_esno(token, ip):
    esno, pls = get_esno_pls(token, ip)
    
    exp_esno = float(read_esno_dict(pls))
    print("#####################")
    print(f"pls: {pls}")
    print(f"current esno: {esno}\nexp. esno: {exp_esno}")
    print("#####################")

    return round(esno - exp_esno, 2), esno, pls, exp_esno


def get_modcod(token, ip):
    signal_pls_code = get_rx_status(token, ip)['test_pattern_pls_code']
    # psk, code = get_modcod_from_pls(signal_pls_code)
    return signal_pls_code


def set_initial_noise(token, ip, pls):
    initial = read_initial_noise(pls)
    if not initial:
        return

    update_noise(token, ip, initial)


def adjustNoise(token, ip):
    pls = get_modcod(token, ip)
    set_initial_noise(token, ip, pls)
    
    distance, current_esno, pls, expected_esno = evaluate_esno(token, ip)
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

        update_noise(token, ip, new_noise)
        
        distance, current_esno, pls, expected_esno = evaluate_esno(token, ip)
    
        distances.update({distance: get_current_noise(token, ip)})
        
        
    print_noise_dict(distances)
    insert_initial_noise(pls, [*distances.values()][-1])
    return f"{pls}"


def get_token(ipaddr):
    
    username = "admin"
    password = "admin"
    token = get_auth(username, password, ipaddr)
    
    if token == -1:
        print("No connection established. exiting program.")
        return
    
    return token


def main():

    modulator_ip = input(f"Enter the ip of the noise finder device. (press enter for {StaticVars.modulator_ip}) ")
    if modulator_ip == '':
        modulator_ip = StaticVars.modulator_ip
        
    token = get_token(modulator_ip)
    
    if token:
        adjustNoise(token, modulator_ip)


if __name__ == "__main__":
    main()
