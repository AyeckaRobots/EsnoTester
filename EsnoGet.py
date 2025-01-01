
import time
from snmp import Engine, SNMPv1


def read_current_esno():

    with Engine(SNMPv1, defaultCommunity=b"public") as engine:
        host = engine.Manager("172.19.200.199")

        load(2)
        
        # just in case something went wrong with the update
        lock = int(host.get(".1.3.6.1.4.1.37576.4.2.1.2.0").toString()[-2])
        while not lock:
            lock = int(host.get(".1.3.6.1.4.1.37576.4.2.1.2.0").toString()[-2])
            time.sleep(0.1)
        
        current_esno = host.get(".1.3.6.1.4.1.37576.4.2.1.3.0")
        return current_esno.toString()


def load(t):
    index = 0
    time_elapsed = 0
    sign = ['/', '-', '\\', '|'] 
    while time_elapsed < t:
        print (f"Loading... [{sign[index]}]", end="\r")
        time.sleep(0.2)
        time_elapsed += 0.2
        index = (index + 1) % 4
            
            


if __name__ == "__main__":
    print(read_current_esno())  # test