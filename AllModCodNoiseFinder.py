from api_request import change_modcod
from NoiseFinder import adjustNoise, get_token
from JsonHandler import read_pls_dict

def get_pls_list():
    
    pls_dict = read_pls_dict()
    pls_list = []
    
    for modulation, codes in pls_dict.items():
        for code, value in codes.items():
            pls_list.append(value)
            
    return pls_list

def set_pls_list():
    pls_list = get_pls_list()
    
    try:
        specific_pls = int(input("Enter specific pls for single test. (press enter for all) "))

        if specific_pls:
            pls_list = [pls_list[(specific_pls-5)//4]]  # works for s2 by ayecka
    except:
        pass
    
    return pls_list


def start_noise_finder(token, ipaddr, pls_list):

    for pls in pls_list:
        change_modcod(token, ipaddr, pls)
        modcod = adjustNoise(token, ipaddr)
        
        print("")
        print(f"Finished for modcod: {modcod}")
        print("")
        

def main():

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