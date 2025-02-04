import paramiko

from SystemUtils.Utils import load


def get_esno():
    # Set up SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown host keys

    # Path to your private key
    private_key_path = r"C:\Users\user\.ssh\id_rsa"

    # Connect to the Raspberry Pi using the private key
    client.connect('192.168.115.78', username='user', key_filename=private_key_path)

    locked = False
    # Run a command (e.g., to check uptime)
    while not locked:
        stdin, lock_stdout, stderr = client.exec_command("snmpget -v1 -c public 172.19.200.199 .1.3.6.1.4.1.37576.4.2.1.2.0")
        lock_stdout = lock_stdout.read().decode()
        # print(lock_stdout)
        locked = int(lock_stdout[-2])
        load(0.2)

    
    stdin, stdout, stderr = client.exec_command("snmpget -v1 -c public 172.19.200.199 .1.3.6.1.4.1.37576.4.2.1.3.0")

    # Read and print the output
    esno = stdout.read().decode()
    # esno = stdout.read().decode()

    # Close the connection
    client.close()

    return esno