from snmp import Engine, SNMPv1

def read_current_esno():

    with Engine(SNMPv1, defaultCommunity=b"public") as engine:
        host = engine.Manager("172.19.200.199")
        current_esno = host.get(".1.3.6.1.4.1.37576.4.2.1.3.0")
        print(current_esno)