import time
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

    return data.json()

def get_advanced_status(token, ip):
    try:
        data = requests.get(f"http://{ip}/api/advanced_status", headers={'Authorization': token})
    except TimeoutError as e:
        print(f"No response from {ip}, error: {e}")
        return -1

    return data.json()

def get_mod(token, ip):
    try:
        data =  requests.get(f"http://{ip}/api/modulator", headers={'Authorization': token})
    except TimeoutError as e:
        print(f"No response from {ip}, error: {e}")
        return -1
    
    return data.json()
    
def get_demod(token, ip):
    try:
        data =  requests.get(f"http://{ip}/api/demodulator", headers={'Authorization': token})
    except TimeoutError as e:
        print(f"No response from {ip}, error: {e}")
        return -1
    
    return data.json()
    
def get_current_noise(token, ip):
    data = [{"address":24688}]
    response = requests.post(f"http://{ip}/api/fpga_read", headers={'Authorization': token}, json=data)

    return response.json()[0]["value"]

def update_mod(token, ip, freq, data:dict=None):
    if data is None:
        data = get_mod(token, ip)
        
    data['frequency'] = freq
    
    requests.post(f"http://{ip}/api/modulator", headers={'Authorization': token}, json=data)
    
def update_demod(token, ip, freq, data:dict=None):
    if data is None:
        data = get_demod(token, ip)
        
    data['frequency'] = freq
    
    requests.post(f"http://{ip}/api/demodulator", headers={'Authorization': token}, json=data)

def update_noise(token, ip, data):
    requests.post(f"http://{ip}/api/fpga_write", headers={'Authorization': token}, json=data)

def main():
    ip = "192.168.15.132"
    username = "admin"
    password = "admin"
    
    auth = get_auth(username, password, ip)
    print(f"Auth:\n{auth}\n\n")
    
    status = get_status(auth, ip)
    """    print(f"status:\n{status}\n\n")
        
        adv_status = get_advanced_status(auth, ip)
        print(f"advanced status:\n{adv_status}\n\n")
        
        mod = get_mod(auth, ip)
        print(f"modulator:\n{mod}\n\n")
        
        demod = get_demod(auth, ip)
        print(f"demodulator:\n{demod}\n\n")
        
        update_mod(auth, ip, 1399000)
        update_demod(auth, ip, 2149000)"""
        
    noise = get_current_noise(auth, ip)
    print(noise)

if __name__ == '__main__':
    main()
  
