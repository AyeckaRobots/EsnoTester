import time

from snmp import Engine, SNMPv1

from ApiRequest import read_esno_api
from SystemUtils.Utils import load


def read_current_esno():
    load(4)
    esno = read_esno_api() / 10
    return esno

# def read_current_esno():
#     """A function to get the current esno read by the novelsat
#     modem using snmp
#
#     Returns:
#         str: the esno read by novelsat modem
#     """
#
#     with Engine(SNMPv1, defaultCommunity=b"public") as engine:
#         host = engine.Manager("172.19.200.199")
#
#         load(2)
#
#         # just in case something went wrong with the update
#         lock = int(host.get(".1.3.6.1.4.1.37576.4.2.1.2.0").toString()[-2])
#         while not lock:
#             lock = int(host.get(".1.3.6.1.4.1.37576.4.2.1.2.0").toString()[-2])
#             time.sleep(0.1)
#
#         current_esno = host.get(".1.3.6.1.4.1.37576.4.2.1.3.0")
#         return int(current_esno.toString().split('(')[1][0:-1]) / 100

#snmpget -v1 -c public 172.19.200.199 .1.3.6.1.4.1.37576.4.2.1.3.0
if __name__ == "__main__":
    print(read_current_esno())  # test