from AllModCodNoiseFinder import start_noise_finder, set_pls_list
from status_requester import start_logging
from NoiseFinder import get_token
import threading

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
    
    time_per_modcod = 200  # 60 seconds
    
    
    pls_list = set_pls_list()
    
    for pls in pls_list:
        
        start_noise_finder(modulator_token, modulator_ip, [pls])
        start_logging(receiver_token, receiver_ip, pls, time_per_modcod)
        
        print("\ndone!")
        
        # noise_finder = threading.Thread(target=start_noise_finder, args=[receiver_token, receiver_ip, [pls]])
        
        
    

if __name__ == "__main__":
    main()