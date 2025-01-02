import time

from api_request import get_advanced_stats, reset_advanced_stats
from JsonHandler import create_result_dict, get_modcod_from_pls, insert_result_dict
from EsnoGet import load
import logging
import keyboard
from datetime import datetime

import threading

current_missed_counter = 0

# read_esno()
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger = logging.getLogger()

logger.setLevel(logging.WARNING)  # change to warning to ignore frame and bit-rate changes and vice versa.


def log_stats(info, current_bit_rate, current_esno, current_frame_counter):
    global current_missed_counter
    
    if info["bit_rate"] != current_bit_rate:
        logging.info(f"Got new bit rate of: {info['bit_rate']}")
    if current_frame_counter > info["frame_counter"]:
        logging.info("Got new frames")
    if current_missed_counter - info["offset"] > info["missed_counter"]:
        logging.warning(f"Missed frames! amount: {current_missed_counter - info['missed_counter'] - info['offset']}, esno: {current_esno}")


def start_logging(token, ip, pls, t=-999):
    global current_missed_counter
    
    reset_advanced_stats(token, ip)
    load(5)
    
    info = {"frame_counter":0 , "missed_counter":0 , "bit_rate":0 , "esno":0, "offset":0, 'done': False}
    
    threading.Thread(target=inputs, args=[info]).start()

    while t > 0 or t <= -999:
        print("sending req (press 'i' for info, 'r' to reset missed)")
        agg = get_advanced_stats(token, ip)

        try:
            if agg == -1:
                continue
            # this is theoretical from here on out. needs testing for agg response.
            current_bit_rate = agg['bit_rate']
            current_esno = agg['esno']  # string (no decimal point, needs division by 10)
            current_frame_counter = agg['frame_counter']
        except KeyError as e:
            print(e)
            continue
        
        try:
            current_missed_counter = agg['missed_counter']
        except KeyError as e:
            current_missed_counter = 0
            
        current_esno = int(current_esno) / 10

        log_stats(info, current_bit_rate, current_esno, current_frame_counter)
        
        info["frame_counter"] = current_frame_counter
        info["missed_counter"] = current_missed_counter - info["offset"]
        info["bit_rate"] = current_bit_rate
        info["esno"] = current_esno
        
        load(10)
        t -= 10  # around 10 seconds have passed
    info['done'] = True
    
    if info["missed_counter"] > 0:
        print(f"⚠︎⚠︎⚠︎ {info["missed_counter"]} frames have been missed! ⚠︎⚠︎⚠︎")
    
    psk, code = get_modcod_from_pls(pls)
    sn = create_result_dict(token, ip)
    insert_result_dict(psk, code, info["missed_counter"], sn)
    

            
def inputs(info: dict):
    
    while not info['done']:
        if keyboard.is_pressed('i'):
            print(f"-----------------------------------------------\nCard Activity Report {datetime.today().strftime('%H:%M:%S')}")
            print(f"Status:\nCurrent frame: {info['frame_counter']}\nAmount missed: {info['missed_counter']}\nCurrent esno {info['esno']}")
            print("-----------------------------------------------")
            time.sleep(1)
        if keyboard.is_pressed('r'):
            reset_missed(info, current_missed_counter)
            time.sleep(1)


def reset_missed(info, current_missed):
    info.update({"missed_counter":0})
    info.update({"offset": current_missed_counter})


def main():
    ipaddress = input("Enter the ip of the device. (just press enter for 192.168.10.200)")
    if ipaddress == '':
        ipaddress = "192.168.10.200"
    start_logging(ipaddress)


if __name__ == "__main__":
    main()