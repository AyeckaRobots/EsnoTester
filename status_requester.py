import time
import threading

import StaticVars
from NoiseFinder import get_token
from api_request import get_advanced_stats, get_serial_number, reset_advanced_stats, update_modulator
from JsonHandler import insert_result_dict
from GlobalFuncs import load
import logging
import keyboard
from datetime import datetime

logger = logging.getLogger()

logger.setLevel(logging.WARNING)  # change to warning to ignore frame and bit-rate changes and vice versa.
current_missed_counter = 0

def init_logger(token, ip):
    """Configuration for the logger

    Args:
        token (str): string for the authorization header
        ip (str): the ip of the tested device
    """
    sn = get_serial_number(token, ip)
    
    logging.basicConfig(filename=f"SN{sn}.log",
                        format='%(asctime)s %(message)s',
                        filemode='a')


def log_stats(info, current_bit_rate, current_esno, current_frame_counter):
    """Log stats to the file, bitrate, new frames and missed frames. 
    (on different levels of logging some might not be logged. (info, warning))

    Args:
        info (dict): dictionary containing the information of the earlier stats
        current_bit_rate (int): value representing the amount of data transfered
        current_esno (int): value representing the current esno.
        current_frame_counter (int): value representing the amount of missed frames
    """
    global current_missed_counter
    
    if info["bit_rate"] != current_bit_rate:
        logging.info(f"Got new bit rate of: {info['bit_rate']}")
    if current_frame_counter > info["frame_counter"]:
        logging.info("Got new frames")
    if current_missed_counter - info["offset"] > info["missed_counter"]:
        logging.warning(f"Missed frames! amount: {current_missed_counter - info['missed_counter'] - info['offset']}, esno: {current_esno}")


def start_logging(token, ip, pls=None, t=-999):
    """A function that checks for missed frames and updates in bitrate and esno
    operating for @t time or endlessly if t=-999. 

    Args:
        token (str): string for the authorization header
        ip (str): the ip of the tested device
        pls (int, optional): the currently tested pls code
        t (int, optional): time to be ran. Defaults to -999 (endless).
    """
    global current_missed_counter
    
    reset_advanced_stats(token, ip)
    load(5)

    info = {"frame_counter":0 , "missed_counter":0 , "bit_rate":0 , "esno":0, "offset":0, 'done': False}
    if pls:
        threading.Thread(target=inputs, args=[info, pls]).start()
    else:
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
            load(2)
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
    
    sn = get_serial_number(token, ip)
    insert_result_dict(pls, info["missed_counter"], sn)
    

            
def inputs(info: dict, pls):
    """A function that checks for user input, if user
    pressed i, print the current status of the device.
    if user pressed r, reset the shown missed frames

    Args:
        info (dict): dictionary containing the information of the stats
        psk (str, optional): the modulation
        code (str, optional): the code
    """
    
    while not info['done']:
        if keyboard.is_pressed('i'):
            print(f"-----------------------------------------------\nCard Activity Report {datetime.today().strftime('%H:%M:%S')}")
            print(f"Status:\nCurrent frame: {info['frame_counter']}\nAmount missed: {info['missed_counter']}\nCurrent esno {info['esno']}")

            print(f"pls: {pls}")

            print("-----------------------------------------------")
            time.sleep(1)
        if keyboard.is_pressed('r'):
            reset_missed(info)
            time.sleep(1)


def reset_missed(info):
    """A function that resets the shown missed frame (only visual)

    Args:
        info (dict): dictionary containing the information of the stats
    """
    info.update({"missed_counter":0})
    info.update({"offset": current_missed_counter})


def main():
    """
    If ran alone, this Python file is used for endlessly checking that the
    device receives new frames and that there are none missing. 
    (ofc if there are it logs the stats to the .log file)
    """

    receiver_ip = input(f"Enter the ip of the tested device. (press enter for {StaticVars.device_ip}) ")
    if receiver_ip == '':
        receiver_ip = StaticVars.device_ip
    
    token = get_token(receiver_ip)
    update_modulator(token, receiver_ip)
    init_logger(token, receiver_ip)
    
    start_logging(token, receiver_ip)


if __name__ == "__main__":
    main()
