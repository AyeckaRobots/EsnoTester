from api_request import change_modcod
from NoiseFinder import adjustNoise, get_token
from JsonHandler import read_pls_dict


def get_pls_list():
    """
    A function that returns a list containing all pls codes for DVBs2

    Returns:
        list: a list containing all pls codes for DVBs2
    """
    
    pls_dict = read_pls_dict()
    pls_list = []
    
    for modulation, codes in pls_dict.items():
        for code, value in codes.items():
            pls_list.append(value)
            
    return pls_list

def set_pls_list():
    """
    A function that reads input from user for specific pls code or all
    pls codes, and returns a list accordingly

    Returns:
        list: pls code list according to the user's input
    """
    pls_list = get_pls_list()
    
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
        modcod = adjustNoise(token, ipaddr)
        
        print("")
        print(f"Finished for modcod: {modcod}")
        print("")
        

def main():
    """
    This Python file is used for finding the correct noise value for
    a single pls code (pls is single-valued to modulation and code)
    or for each and every modulation and code (modcod)
    such that the target esno and the measured esno are almost identical
    """
    
    ipaddr = input("Enter the ip of the device. (press enter for 192.168.15.10) ")
    if ipaddr == '':
        ipaddr = "192.168.15.10"
        
    token = get_token(ipaddr)
    
    if not token:
        return
    
    pls_list = set_pls_list()
    start_noise_finder(token, ipaddr, pls_list)
    
        
if __name__ == "__main__":
    main()