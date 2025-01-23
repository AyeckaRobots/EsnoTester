from SystemUtils import StaticVars
from ApiRequest import change_modcod, update_modulator
from SystemComponents.NoiseFinder import adjustNoise, get_token

def set_pls_list(pls_list):
    """
    A function that reads input from user for specific pls code or all
    pls codes, and returns a list accordingly

    Returns:
        list: pls code list according to the user's input
    """

    try:
        specific_pls = int(input("Enter specific pls for single test. (press enter for all) "))

        if specific_pls in pls_list:
            pls_list = [specific_pls]
    except:
        pass

    return pls_list


def start_noise_finder(token, ipaddr, pls_list):
    """A function that reaches to the sm1x web api and
    checks for each pls in @pls_list what the correct noise value is

    Args:
        token (str): the auth token for the api
        ipaddr (str): the ip of the api server
        pls_list (list): list of pls codes to iterate over
    """
    for pls in pls_list:
        change_modcod(token, ipaddr, pls)
        pls = adjustNoise(token, ipaddr)
        
        print("")
        print(f"Finished for pls: {pls}")
        print("")
        

def main():
    """
    This Python file is used for finding the correct noise value for
    a single pls code (pls is single-valued to modulation and code)
    or for each and every modulation and code (modcod)
    such that the target esno and the measured esno are almost identical
    """

    modulator_ip = input(f"Enter the ip of the noise finder device. (press enter for {StaticVars.modulator_ip}) ")
    if modulator_ip == '':
        modulator_ip = StaticVars.modulator_ip
        
    token = get_token(modulator_ip)
    
    if not token:
        return

    pls_list = set_pls_list(StaticVars.all_pls_simplified)
    start_noise_finder(token, modulator_ip, pls_list)
    
        
if __name__ == "__main__":
    main()