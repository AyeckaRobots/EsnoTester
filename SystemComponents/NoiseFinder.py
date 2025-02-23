from SystemUtils import StaticVars
from Requests import *
from JsonHandler import *

max_noise = -40  # 1c200
min_noise = 25  # 1c000
esno_offset = 0.3
allowed_esno_error = StaticVars.esno_acceptable
error_multiplier = 1

def print_noise_dict(distances):
    for key, value in dict.items(distances):         
        print(f"esno distance: {key}, on noise: {value}")


def evaluate_esno_distance(pls):
    esno = get_esno()
    while int(esno) == -10:
        load(2)
        esno = get_esno()

    
    exp_esno = float(read_esno_dict(pls))
    print("#####################")
    print(f"pls: {pls}")
    print(f"current esno: {esno}\nexp. esno: {exp_esno}")
    print("#####################")

    return round(esno - exp_esno - esno_offset, 2), exp_esno + esno_offset


def get_modcod():
    signal_pls_code = "gRPC" # get_rx_status(token, ip)['test_pattern_pls_code']
    # psk, code = get_modcod_from_pls(signal_pls_code)
    return signal_pls_code


def set_initial_noise(pls):
    initial = read_initial_noise(pls)
    if not initial:
        return

    set_noise(initial)


def adjustNoise(pls):
    first_noise = get_noise()

    distance, exp_esno = evaluate_esno_distance(pls)

    set_noise(round(first_noise + distance, 3))
    current_noise = get_esno()

    while abs(current_noise - exp_esno) > allowed_esno_error:
        load(5)
        current_noise = get_esno()
        print(f"Current noise: {current_noise}")
    # set_initial_noise(pls)
    
    # distance = evaluate_esno_distance(pls)
    # # try:
    # #     esno_multiplier_rate = max(1, min(3, abs(4 / expected_esno))) #######
    # # except ZeroDivisionError as e:
    # #     esno_multiplier_rate = 1
    # esno_multiplier_rate = 1

    # distances = {distance: get_noise()}
    # while abs(distance) > allowed_esno_error:
    #     print_noise_dict(distances)
    #     load(5)
    #     new_noise = int(max(min_noise, min(max_noise, distances[distance] + distance*error_multiplier*esno_multiplier_rate)))

    #     set_noise(new_noise)
        
    #     distance = evaluate_esno_distance(pls)
    
    #     distances.update({distance: get_noise()})
        
    # print_noise_dict(distances)
    # insert_initial_noise(pls, [*distances.values()][-1])

    return f"{pls}"


def main():

    #read_target_ip("modulator")

    adjustNoise()


if __name__ == "__main__":
    main()
