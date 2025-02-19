
import sys
sys.path.append('/home/user/Documents/EsnoTester/SystemUtils/GRpc')  # nopep8
# from SystemComponents.AllModCodNoiseFinder import set_pls_list, start_noise_finder
from SystemUtils.Utils import update_pls_list
# from Requests import update_noise
from SystemComponents.status_requester import start_logging, init_logger

import os
from SystemUtils import StaticVars


def set_standard(standard, adjust_noise=False):
    pls_list = update_pls_list(standard)
    start_sm1x_tester(pls_list, adjust_noise)


def start_sm1x_tester(pls_list, adjust_noise=False):
    # pls_list = set_pls_list(pls_list)

    # if not adjust_noise:
    #     update_noise(0)

    for pls in pls_list:
        # if adjust_noise:
            # start_noise_finder([pls])

        start_logging(pls, StaticVars.time_per_modcod)

        print(f"\npls {pls} done!")


def clear_logfile():
    """removes the logfile if it exists

    Args:
        token (str): string for the authorization header
        ip (str): the ip of the tested device
    """

    if os.path.exists(f"Report.log"):
        os.remove(f"Report.log")
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

    # modulator_ip = input(f"Enter the ip of the noise finder device. (press enter for {read_target_ip('modulator')}) ")
    # if modulator_ip == '':
    #     modulator_ip = read_target_ip("modulator")

    # modulator_token = get_token(modulator_ip)

    # if not modulator_token:
    #     return

    # update_target_ip('modulator', modulator_ip)

    # receiver_ip = input(f"Enter the ip of the tested device. (press enter for {read_target_ip('receiver')}) ")
    # if receiver_ip == '':
    #     receiver_ip = read_target_ip("receiver")

    # receiver_token = get_token(receiver_ip)

    # if not receiver_token:
    #     return

    # update_target_ip('receiver', receiver_ip)

    standard = input("write standard to go through, s2 or s2x. (press enter for both) ")

    check_esno = check_esno_input()

    # set_freq(modulator_token, modulator_ip, receiver_token, receiver_ip, 1200)

    clear_logfile()
    init_logger()

    set_standard(standard, check_esno)



if __name__ == "__main__":
    main()
