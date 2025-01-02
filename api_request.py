
import requests


def get_auth(username, password, ip):
    try:
        response = requests.post(f"http://{ip}/api/login", json={"username": username, "password": password})
    except TimeoutError as e:
        print(f"couldn't connect to ip: {ip} ")
        return -1
    return f"Bearer {response.json()['token']}"


def get_status(token, ip):
    try:
        data = requests.get(f"http://{ip}/api/settings", headers={'Authorization': token})
    except TimeoutError as e:
        print(f"No response from {ip}, error: {e}")
        return -1

    return data.json()['tx']


def get_serial_number(token, ip):
    try:
        data = requests.get(f"http://{ip}/api/status", headers={'Authorization': token})
    except TimeoutError as e:
        print(f"No response from {ip}, error: {e}")
        return -1

    return data.json()['serial_number']


def get_current_noise(token, ip):
    data = [{"address":24688}]
    response = requests.post(f"http://{ip}/api/fpga_read", headers={'Authorization': token}, json=data)
    # print(response.json())
    return response.json()[0]["value"]


def get_advanced_stats(token, ip):
    try:
        data = requests.get(f"http://{ip}/api/advanced_status", headers={'Authorization': token})
    except TimeoutError as e:
        print(f"No response from {ip}, error: {e}")
        return -1

    # print("agg: ", data.json()["agg_slices"][0])
    return data.json()["agg_slices"][0]


def update_noise(token, ip, data):
    requests.post(f"http://{ip}/api/fpga_write", headers={'Authorization': token}, json=data)
    
    
def update_modulator(token, ip):
    data = {"enable":True,"frequency":1200000,"symbol_rate":12000,
            "power":-30,"roll_off":"Alpha_020","spectral_inversion":False,
            "gold_code":0,"carrier_mode":"CM_MODULATED","power_up_state":"On",
            "acm_mode":"AcmModeOff","buc_power":False,"buc_10MHz_output":False}
    response = requests.post(f"http://{ip}/api/modulator", headers={'Authorization': token}, json=data)
    

def change_modcod(token, ip, pls):
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
    requests.get(f"http://{ip}/api/reset_advanced_status", headers={'Authorization': token})
