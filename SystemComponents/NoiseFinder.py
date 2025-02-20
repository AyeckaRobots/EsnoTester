from SystemUtils import StaticVars
from Requests import *
from JsonHandler import *

max_noise = 115232  # 1c220
min_noise = 114688  # 1c000
allowed_esno_error = StaticVars.esno_acceptable
error_multiplier = 10

def print_noise_dict(distances):
    for key, value in dict.items(distances):         
        print(f"esno distance: {key}, on noise: {value}, hex: {hex(value)}")
        

def get_esno_pls():
    esno = get_esno()
    
    pls = get_modcod() # Novelsat
    return esno, pls


def evaluate_esno():
    esno, pls = get_esno_pls()
    
    exp_esno = float(read_esno_dict(pls))
    print("#####################")
    print(f"pls: {pls}")
    print(f"current esno: {esno}\nexp. esno: {exp_esno}")
    print("#####################")

    return round(esno - exp_esno, 2), esno, pls, exp_esno


def get_modcod():
    signal_pls_code = "gRPC" # get_rx_status(token, ip)['test_pattern_pls_code']
    # psk, code = get_modcod_from_pls(signal_pls_code)
    return signal_pls_code


def set_initial_noise(pls):
    initial = read_initial_noise(pls)
    if not initial:
        return

    set_noise(initial)


def adjustNoise():
    pls = get_modcod()
    set_initial_noise(pls)
    
    distance, current_esno, pls, expected_esno = evaluate_esno()
    try:
        esno_multiplier_rate = max(1, min(3, abs(4 / expected_esno)))
    except ZeroDivisionError as e:
        esno_multiplier_rate = 2

    distances = {distance: get_noise()}
    while abs(distance) > allowed_esno_error:
        print_noise_dict(distances)
            
        new_noise = int(max(min_noise, min(max_noise, distances[distance] + distance*error_multiplier*esno_multiplier_rate)))

        set_noise(new_noise)
        
        distance, current_esno, pls, expected_esno = evaluate_esno()
    
        distances.update({distance: get_noise()})
        
        
    print_noise_dict(distances)
    insert_initial_noise(pls, [*distances.values()][-1])
    return f"{pls}"


def main():

    #read_target_ip("modulator")

    adjustNoise()


if __name__ == "__main__":
    main()
