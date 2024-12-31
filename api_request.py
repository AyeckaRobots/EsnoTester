
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
        data = requests.get(f"http://{ip}/api/status", headers={'Authorization': token})
    except TimeoutError as e:
        print(f"No response from {ip}, error: {e}")
        return -1

    return data.json()['tx']


def get_current_noise(token, ip):
    data = [{"address":24688}]
    response = requests.post(f"http://{ip}/api/fpga_read", headers={'Authorization': token}, json=data)
    # print(response.json())
    return response.json()[0]["value"]


def update_noise(token, ip, data):
    requests.post(f"http://{ip}/api/fpga_write", headers={'Authorization': token}, json=data)
    
    
def update_modulator(token, ip):
    data = {"enable":True,"frequency":1200000,"symbol_rate":12000,
            "power":-30,"roll_off":"Alpha_020","spectral_inversion":False,
            "gold_code":0,"carrier_mode":"CM_MODULATED","power_up_state":"On",
            "acm_mode":"AcmModeOff","buc_power":False,"buc_10MHz_output":False}
    response = requests.post(f"http://{ip}/api/modulator", headers={'Authorization': token}, json=data)
    

def change_modcod(token, ip, pls):
    data = [{"index":0,"enable":True,"pls_code":pls,"isi":0,"label":"D0:D1:D2:D3:D4:D5","label_type":"6-Byte","vlan":4096}]
    response = requests.post(f"http://{ip}/api/encapsulator", headers={'Authorization': token}, json=data)