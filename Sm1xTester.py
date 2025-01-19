from AllModCodNoiseFinder import start_noise_finder, set_pls_list, get_pls_list
from api_request import get_serial_number, set_freq, update_noise
from status_requester import init_logger, start_logging
from NoiseFinder import get_token
from JsonHandler import update_standard
import os
import StaticVars



def set_standard(modulator_token, modulator_ip, receiver_token, receiver_ip, standard, adjust_noise=False):
    if standard == '':
        update_standard('s2')
        start_sm1x_tester(modulator_token, modulator_ip, receiver_token, receiver_ip, adjust_noise)
        update_standard('s2x')
        start_sm1x_tester(modulator_token, modulator_ip, receiver_token, receiver_ip, adjust_noise, skip_pls_selection=True)

    elif standard == 's2' or standard == 's2x':
        update_standard(standard)
        start_sm1x_tester(modulator_token, modulator_ip, receiver_token, receiver_ip, adjust_noise)

    else:
        print("Invalid standard, exiting program...")


def start_sm1x_tester(modulator_token, modulator_ip, receiver_token, receiver_ip, adjust_noise=False, skip_pls_selection=False):
    time_per_modcod = 30  # 60 seconds
    if skip_pls_selection:
        pls_list = get_pls_list()
    else:
        pls_list = set_pls_list()

    if not adjust_noise:
        update_noise(modulator_token, modulator_ip, 0)

    for pls in pls_list:
        if adjust_noise:
            start_noise_finder(modulator_token, modulator_ip, [pls])

        start_logging(receiver_token, receiver_ip, pls, time_per_modcod)

        print(f"\npls {pls} done!")


def clear_logfile(token, ip):
    """removes the logfile if it exists

    Args:
        token (str): string for the authorization header
        ip (str): the ip of the tested device
    """
    sn = get_serial_number(token, ip)

    if os.path.exists(f"SN{sn}.log"):
        os.remove(f"SN{sn}.log")
    else:
        return


def check_esno_input():
    adjust_noise = ""
    while adjust_noise != 'y' and adjust_noise != 'n':
        adjust_noise = input("Do you want the noise to be adjusted to ideal level? (y/n) ")
    if adjust_noise == "y":
        return True
    else:
        return False


def main():
    """
    This Python file is used for testing what modcods does the Sm1x connected pass with no missed frames and what modcods
    it fails.
    """
    
    modulator_ip = input(f"Enter the ip of the noise finder device. (press enter for {StaticVars.modulator_ip}) ")
    if modulator_ip == '':
        modulator_ip = StaticVars.modulator_ip
    
    modulator_token = get_token(modulator_ip)
    
    if not modulator_token:
        return
    
    
    receiver_ip = input(f"Enter the ip of the tested device. (press enter for {StaticVars.device_ip}) ")
    if receiver_ip == '':
        receiver_ip = StaticVars.device_ip
    
    receiver_token = get_token(receiver_ip)
    
    if not receiver_token:
        return

    standard = input("write standard to go through, s2 or s2x. (press enter for both) ")

    check_esno = check_esno_input()

    set_freq(modulator_token, modulator_ip, receiver_token, receiver_ip, 1200)

    clear_logfile(receiver_token, receiver_ip)
    init_logger(receiver_token, receiver_ip)

    set_standard(modulator_token, modulator_ip, receiver_token, receiver_ip, standard, check_esno)



if __name__ == "__main__":
    main()
