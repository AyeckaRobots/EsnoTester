"""
This file is a collection of function that use requests to communicate
with the api server in order to extract and change information
these functions are used throughout the codebase.
"""
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

import sys
sys.path.append('SystemUtils/GRpc')  # nopep8

snmp_requests = {
    "pilots": ".1.3.6.1.4.1.37576.3.1.2.1.1.7.1", #0=no 1=yes
    "frame": ".1.3.6.1.4.1.37576.3.1.2.1.1.4.1",#0=normal 1=short
    "mod": ".1.3.6.1.4.1.37576.3.1.2.1.1.5.1",#modulationBpsk (0),modulationQpsk (1),modulation8Psk (2),modulation16Qam (3),modulation16Apsk (4),
    #modulation32Apsk (5),modulation64Apsk (6),modulation128Apsk(7),modulation256Apsk(8),modulation8ApskL (9),modulation16ApskL (10),
    # modulation32ApskL (11),modulation64ApskL (12),modulation256ApskL(13),notApplicable (255)

    "cod": ".1.3.6.1.4.1.37576.3.1.2.1.1.6.1"#fec1Div4 (1),fec1Div3 (2),fec2Div5 (3),fec13Div30 (4),fec4Div9 (5),fec7Div15 (6),fec22Div45 (7),fec1Div2 (8),fec8Div15 (9)
    #,fec5Div9 (10),fec17Div30 (11),fec3Div5 (12),fec28Div45 (13),fec19Div30 (14),fec2Div3 (15),fec32Div45 (16),fec11Div15 (17),fec3Div4 (18),fec7Div9 (19),fec4Div5 (20),
    # fec37Div45 (21),fec5Div6 (22),fec7Div8 (23),fec8Div9 (24),fec9Div10 (25),fec11Div45 (26),fec4Div15 (27),fec13Div45 (28),fec14Div45 (29),fec9Div20 (30),fec11Div20 (31),fec26Div45 (32),fec23Div36 (33),fec29Div45 (34),fec31Div45 (35),fec25Div36 (36),fec13Div18 (37),fec77Div90 (38),notApplicable (255)
}

str_to_snmp_value = {
    #PILOTS
    "true": "1",
    "True": "1",
    "false": "0",
    "False": "0",
    #"FRAME"
    "Normal": "0",
    "Short": "1",
    #"MODULATION"
    "QPSK": "1",
    "8PSK": "2",
    "16APSK": "4",
    "32APSK": "5",
    "64APSK": "6",
    "128APSK": "7",
    "256APSK": "8",
    "8APSKL": "9",
    "16APSKL": "10",
    "32APSKL": "11",
    "64APSKL": "12",
    "256APSKL": "13",
    #"CODE"
    "1/4": "1",
    "1/3": "2",
    "2/5": "3",
    "13/30": "4",
    "4/9": "5",
    "7/15": "6",
    "22/45": "7",
    "1/2": "8",
    "8/15": "9",
    "5/9": "10",
    "17/30": "11",
    "3/5": "12",
    "28/45": "13",
    "19/30": "14",
    "2/3": "15",
    "32/45": "16",
    "11/15": "17",
    "3/4": "18",
    "7/9": "19",
    "4/5": "20",
    "37/45": "21",
    "5/6": "22",
    "7/8": "23",
    "8/9": "24",
    "9/10": "25",
    "11/45": "26",
    "4/15": "27",
    "13/45": "28",
    "14/45": "29",
    "9/20": "30", 
    "11/20": "31",
    "26/45": "32",
    "23/36": "33",
    "29/45": "34",
    "31/45": "35",
    "25/36": "36",
    "13/18": "37",
    "77/90": "38",
}


# print(sys.path)
import grpc
from google.protobuf import wrappers_pb2
from SystemUtils.GRpc.board_pb2_grpc import *
from SystemUtils.GRpc.board_pb2 import *
from SystemUtils.Utils import load
from snmp import Engine, SNMPv1, SNMPv2c#, ObjectIdentity, ObjectType
from JsonHandler import read_pls_dict, read_target_ip

def get_tc_status(id=1):

    channel = grpc.insecure_channel(f'{read_target_ip("receiver")}:51001')
    stub = BoardServiceStub(channel)

    request = wrappers_pb2.Int32Value(value=id)
    response = stub.GetPeriodicReport(request)
    return response

def snmp_get(OID):
    
    with Engine(SNMPv1, defaultCommunity=b"public") as engine:
        host = engine.Manager(read_target_ip("modulator"))

        return host.get(OID)

async def snmp_set(OID, data: int):
    errorIndication, errorStatus, errorIndex, varBinds = await set_cmd(
        SnmpEngine(),
        CommunityData('private'),
        await UdpTransportTarget.create(('172.19.4.196', 161)),
        ContextData(),
        ObjectType(ObjectIdentity(OID), Integer(data))
    )

def get_esno():
    status = get_tc_status()
    return status.periodic_report.translated_cnr


def set_noise(noise):
    ...
def get_noise():
    ...

def change_modcod(pls):
    """A function to get the current esno read by the novelsat
    modem using snmp

    Returns:
        str: the esno read by novelsat modem
    """
    pls_dict = read_pls_dict(pls)
    if "-L" in pls_dict['code']:
        pls_dict['code'] = pls_dict['code'][:-2]  # removes the -L
        pls_dict['modulation'] = pls_dict['modulation'] + "L"
    print(pls_dict) # debug
    # print(snmp_get(".1.3.6.1.4.1.37576.1.0"))

    asyncio.run(snmp_set(snmp_requests["mod"], str_to_snmp_value[pls_dict['modulation']]))
    asyncio.run(snmp_set(snmp_requests["cod"], str_to_snmp_value[pls_dict['code']]))
    asyncio.run(snmp_set(snmp_requests["frame"], str_to_snmp_value[pls_dict['frame']]))
    asyncio.run(snmp_set(snmp_requests["pilots"], str_to_snmp_value[f"{pls_dict['pilots']}"]))
    
    print("SET!")
# def get_auth(username, password, ip):
#     """A function to get an auth token for the api server

#     Args:
#         username (str): the username for the login page
#         password (str): the password for the login page
#         ip (str): the ip of the api server

#     Returns:
#         str: a string for the authorization header
#     """
#     try:
#         response = requests.post(f"http://{ip}/api/login", json={"username": username, "password": password})
#     except TimeoutError as e:
#         print(f"couldn't connect to ip: {ip} ")
#         return -1
#     return f"Bearer {response.json()['token']}"


# def get_rx_status(token, ip):
#     """A function that retrieves the rx status data of the device

#     Args:
#         token (str): string for the authorization header
#         ip (str): the ip of the api server

#     Returns:
#         success:   dict: the current status of the rx component
#         fail:   int: -1 representing failed communication with the api server
#     """
#     try:
#         data = requests.get(f"http://{ip}/api/settings", headers={'Authorization': token})
#     except TimeoutError as e:
#         print(f"No response from {ip}, error: {e}")
#         return -1

#     return data.json()['tx']


# def get_serial_number(token, ip):
#     """A function that retrieves the serial number of the device

#     Args:
#         token (str): string for the authorization header
#         ip (str): the ip of the api server

#     Returns:
#         success:   int: the serial number of the device being tested
#         fail:   int: -1 representing failed communication with the api server
#     """
#     try:
#         data = requests.get(f"http://{ip}/api/status", headers={'Authorization': token})
#     except TimeoutError as e:
#         print(f"No response from {ip}, error: {e}")
#         return -1

#     return data.json()['serial_number']


# def get_current_noise(token, ip):
#     """A function that retrieves the current noise that is
#     being used. 

#     Args:
#         token (str): string for the authorization header
#         ip (str): the ip of the api server

#     Returns:
#         int: the noise value currently being used
#     """
#     data = [{"address":24688}]
#     response = requests.post(f"http://{ip}/api/fpga_read", headers={'Authorization': token}, json=data)
#     return response.json()[0]["value"]


def get_advanced_stats():
    """A function that retrieves the advanced status data of the device

    Args:
        token (str): string for the authorization header
        ip (str): the ip of the api server

    Returns:
        success:   dict: the current status of the test signal
        fail:   int: -1 representing failed communication with the api server
    """
    status = get_tc_status()
    return {
        "frame_counter" : status.nspe2.frame_count,
         "bit_rate" : status.nspe2.data_rate,
         "missed_counter" : status.nspe2.crc_error_count,
         "esno": status.periodic_report.translated_cnr
         }



# def update_noise(token, ip, value):
#     """A function that sets a fpga parameter according to the @data passed 
#     (currently used to update the noise) 

#     Args:
#         token (str): string for the authorization header
#         ip (str): the ip of the api server
#         value (int): the new noise value for fpga to set.
#     """
#     data = [{"address":24688, "value": value}]
#     requests.post(f"http://{ip}/api/fpga_write", headers={'Authorization': token}, json=data)
    
    
# def set_modulator_freq_1200M(token, ip):
#     """A function that sets the moducaltor (tx) frequency to 1200M 
#     (neccesery for the test) all other variables are changeable
#     but were coppied from the website for the post request to work.

#     Args:
#         token (str): string for the authorization header
#         ip (str): the ip of the api server
#     """
#     data = {"enable":True,"frequency":1200000,"symbol_rate":12000,
#             "power":-30,"roll_off":"Alpha_020","spectral_inversion":False,
#             "gold_code":0,"carrier_mode":"CM_MODULATED","power_up_state":"On",
#             "acm_mode":"AcmModeOff","buc_power":False,"buc_10MHz_output":False}
#     response = requests.post(f"http://{ip}/api/modulator", headers={'Authorization': token}, json=data)

# def reset_advanced_stats(token, ip):
#     """A function that resets the advanced stats back to 0's
#     when testing and checking for missed frames it is important to reset it.

#     Args:
#         token (str): string for the authorization header
#         ip (str): the ip of the api server
#     """
#     requests.get(f"http://{ip}/api/reset_advanced_status", headers={'Authorization': token})

# def set_freq(modulator_token, modulator_ip, receiver_token, receiver_ip, freq):
#     data = {"enable": True, "frequency": freq*1000, "symbol_rate": 12000,
#             "power": -30, "roll_off": "Alpha_020", "spectral_inversion": False,
#             "gold_code": 0, "carrier_mode": "CM_MODULATED", "power_up_state": "On",
#             "acm_mode": "AcmModeOff", "buc_power": False, "buc_10MHz_output": False}
#     data2 = {"frequency":freq*1000,"acquisition_range":2000,"symbol_rate":12000,"force_relock":True,
#              "acm_manager":"127.0.0.1","lnb_settings":
#              [{"lnb_1v_compensation":False,"lnb_reference":"R_OFF", "lnb_tone":"T_OFF", "lnb_voltage":"V_OFF","rf_source":2},
#              {"lnb_1v_compensation":False,"lnb_tone":"T_OFF","lnb_voltage":"V_OFF","rf_source":1,"lnb_reference":"R_OFF"}]
#              ,"rf_source":1,"roll_off":"RT_AUTO","acm_mode":"AcmModeFollowTx","acm_frame_length":"AcmNormalFrame","gold_code":0}

#     requests.post(f"http://{modulator_ip}/api/modulator", headers={'Authorization': modulator_token}, json=data)
#     requests.post(f"http://{receiver_ip}/api/demodulator", headers={'Authorization': receiver_token},json=data2)



