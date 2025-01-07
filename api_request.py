"""
This file is a collection of function that use requests to communicate
with the api server in order to extract and change information
these functions are used throughout the codebase.
"""
import requests


def get_auth(username, password, ip):
    """A function to get an auth token for the api server

    Args:
        username (str): the username for the login page
        password (str): the password for the login page
        ip (str): the ip of the api server

    Returns:
        str: a string for the authorization header
    """
    try:
        response = requests.post(f"http://{ip}/api/login", json={"username": username, "password": password})
    except TimeoutError as e:
        print(f"couldn't connect to ip: {ip} ")
        return -1
    return f"Bearer {response.json()['token']}"


def get_rx_status(token, ip):
    """A function that retrieves the rx status data of the device

    Args:
        token (str): string for the authorization header
        ip (str): the ip of the api server

    Returns:
        success:   dict: the current status of the rx component
        fail:   int: -1 representing failed communication with the api server
    """
    try:
        data = requests.get(f"http://{ip}/api/settings", headers={'Authorization': token})
    except TimeoutError as e:
        print(f"No response from {ip}, error: {e}")
        return -1

    return data.json()['tx']


def get_serial_number(token, ip):
    """A function that retrieves the serial number of the device

    Args:
        token (str): string for the authorization header
        ip (str): the ip of the api server

    Returns:
        success:   int: the serial number of the device being tested
        fail:   int: -1 representing failed communication with the api server
    """
    try:
        data = requests.get(f"http://{ip}/api/status", headers={'Authorization': token})
    except TimeoutError as e:
        print(f"No response from {ip}, error: {e}")
        return -1

    return data.json()['serial_number']


def get_current_noise(token, ip):
    """A function that retrieves the current noise that is
    being used. 

    Args:
        token (str): string for the authorization header
        ip (str): the ip of the api server

    Returns:
        int: the noise value currently being used
    """
    data = [{"address":24688}]
    response = requests.post(f"http://{ip}/api/fpga_read", headers={'Authorization': token}, json=data)
    return response.json()[0]["value"]


def get_advanced_stats(token, ip):
    """A function that retrieves the advanced status data of the device

    Args:
        token (str): string for the authorization header
        ip (str): the ip of the api server

    Returns:
        success:   dict: the current status of the test signal
        fail:   int: -1 representing failed communication with the api server
    """
    try:
        data = requests.get(f"http://{ip}/api/advanced_status", headers={'Authorization': token})
    except TimeoutError as e:
        print(f"No response from {ip}, error: {e}")
        return -1

    return data.json()["agg_slices"][0]


def update_noise(token, ip, data):
    """A function that sets a fpga parameter according to the @data passed 
    (currently used to update the noise) 

    Args:
        token (str): string for the authorization header
        ip (str): the ip of the api server
        data (dict): the location and new value for the fpga
    """
    requests.post(f"http://{ip}/api/fpga_write", headers={'Authorization': token}, json=data)
    
    
def update_modulator(token, ip):
    """A function that sets the moducaltor (tx) frequency to 1200M 
    (neccesery for the test) all other variables are changeable
    but were coppied from the website for the post request to work.

    Args:
        token (str): string for the authorization header
        ip (str): the ip of the api server
    """
    data = {"enable":True,"frequency":1200000,"symbol_rate":12000,
            "power":-30,"roll_off":"Alpha_020","spectral_inversion":False,
            "gold_code":0,"carrier_mode":"CM_MODULATED","power_up_state":"On",
            "acm_mode":"AcmModeOff","buc_power":False,"buc_10MHz_output":False}
    response = requests.post(f"http://{ip}/api/modulator", headers={'Authorization': token}, json=data)
    

def change_modcod(token, ip, pls):
    """A function that sets the modcod of the device to the given pls
    (each pls corresponeds to a modcod)

    Args:
        token (str): string for the authorization header
        ip (str): the ip of the api server
        pls (int): the pls to set
    """
    data = {"system":{"description":"","device":"SM1X","external_10MHz_clock_source":False,
                  "minimal_free_disk_space":50,"symbol_rate_ranges":[30000,60000,120000,240000],
                  "temperature_threshold":60,"tod":{"enable":True,"internal":False},"version_history":4},
            "rx":{"acm_max_pls":"16APSK","acm_max_pls_options":["N/A","QPSK","8APSK","16APSK","32APSK","64APSK","128APSK","256APSK"],
                  "annex_m":False,"configuration_delay":0,"egress":{"destination_ip":"225.21.21.21","destination_port":2121,"source_port":1212},
                  "ldpc_capacity":180,"pls_filter":"OFF","reconfigure_attempts":0,"search_mode":"SAT_COLD","slices":16,
                  "symbol_rate":{"min":100,"max":460000},"test_pattern_type":"Simple"},
            "tx":{"acm_link_margin":10,"annex_m":False,"aupc":False,"packetization_delay":1,"sdfec_on":False,"symbol_rate":{"min":100,"max":460000},
                  "test_pattern_pls_code":pls,"test_pattern_slice":0,"test_pattern_type":"Simple"}}

    response = requests.post(f"http://{ip}/api/settings", headers={'Authorization': token}, json=data)
    
    
def reset_advanced_stats(token, ip):
    """A function that resets the advanced stats back to 0's
    when testing and checking for missed frames it is important to reset it.

    Args:
        token (str): string for the authorization header
        ip (str): the ip of the api server
    """
    requests.get(f"http://{ip}/api/reset_advanced_status", headers={'Authorization': token})
