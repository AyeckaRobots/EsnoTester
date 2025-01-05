from AllModCodNoiseFinder import start_noise_finder, set_pls_list
from api_request import get_serial_number
from status_requester import init_logger, start_logging
from NoiseFinder import get_token
import os


def main():
    
    modulator_ip = input("Enter the ip of the noise finder device. (press enter for 192.168.15.10) ")
    if modulator_ip == '':
        modulator_ip = "192.168.15.10"
    
    modulator_token = get_token(modulator_ip)
    
    if not modulator_token:
        return
    
    
    receiver_ip = input("Enter the ip of the tested device. (press enter for 192.168.10.200) ")
    if receiver_ip == '':
        receiver_ip = "192.168.10.200"
    
    receiver_token = get_token(receiver_ip)
    
    if not receiver_token:
        return
    
    time_per_modcod = 60  # 60 seconds
    
    
    pls_list = set_pls_list()
    
    clear_logfile(receiver_token, receiver_ip)
    init_logger(receiver_token, receiver_ip)
    
    for pls in pls_list:
        
        start_noise_finder(modulator_token, modulator_ip, [pls])
        start_logging(receiver_token, receiver_ip, pls, time_per_modcod)
        
        print("\ndone!")
        
        # noise_finder = threading.Thread(target=start_noise_finder, args=[receiver_token, receiver_ip, [pls]])
        
        
def clear_logfile(token, ip):
    sn = get_serial_number(token, ip)
    
    if os.path.exists(f"SN{sn}.log"):
        os.remove(f"SN{sn}.log")
    else:
        return  


if __name__ == "__main__":
    main()
