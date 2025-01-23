
from JsonHandler import set_token_json, read_target_ip, update_target_ip
from ApiRequest import get_serial_number, set_freq
from SystemComponents.status_requester import init_logger
from SystemComponents.NoiseFinder import get_token
from SystemComponents.Sm1xTester import set_standard, check_esno_input
import os



def main():
    """
    This Python file is used for testing what modcods does the Sm1x connected pass with no missed frames and what modcods
    it fails.
    """

    modulator_ip = input(f"Enter the ip of the noise finder device. (press enter for {read_target_ip('modulator')}) ")
    if modulator_ip == '':
        modulator_ip = read_target_ip("modulator")

    modulator_token = get_token(modulator_ip)

    if not modulator_token:
        return

    update_target_ip('modulator', modulator_ip)

    receiver_ip = input(f"Enter the ip of the tested device. (press enter for {read_target_ip('receiver')}) ")
    if receiver_ip == '':
        receiver_ip = read_target_ip("receiver")

    receiver_token = get_token(receiver_ip)

    if not receiver_token:
        return

    update_target_ip('receiver', receiver_ip)

    try:
        freq = input("write a frequency between 950 and 2150. (press enter for all)")
    except:
        freq = 1200
        print("Invalid frequency, set to 1200")

    standard = input("write standard to go through, s2 or s2x. (press enter for both)")

    check_esno = check_esno_input()
    set_token_json(receiver_token,modulator_token)
    clear_logfile(receiver_token, receiver_ip)
    init_logger(receiver_token, receiver_ip)

    if freq == '':
        for i in range (1,25):
            set_freq(modulator_token, modulator_ip, receiver_token, receiver_ip, i*50 + 900)
            set_standard(modulator_token, modulator_ip, receiver_token, receiver_ip, standard, check_esno)

    elif 950 <= int(freq) <= 2150:
        set_freq(modulator_token, modulator_ip, receiver_token, receiver_ip, int(freq))
        set_standard(modulator_token, modulator_ip, receiver_token, receiver_ip, standard, check_esno)

    else:
        print("Invalid frequency, exiting program...")


def clear_logfile(token, ip):
    """removes the logfile if it exists

    Args:
        token (str): string for the authorization header
        ip (str): the ip of the tested device
    """
    sn = get_serial_number(token, ip)

    if os.path.exists(f"TestResults/SN{sn}.log"):
        os.remove(f"TestResults/SN{sn}.log")
    else:
        return


if __name__ == "__main__":
    main()
