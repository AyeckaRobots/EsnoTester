import paramiko

from SystemUtils.Utils import load


def get_esno():
    # Set up SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown host keys

    # Path to your private key
    private_key_path = r"C:\Users\user\.ssh\id_rsa"

    # Connect to the Raspberry Pi using the private key
    client.connect('192.168.115.49', username='user', key_filename=private_key_path)

    locked = False
    # Run a command (e.g., to check uptime)
    while not locked:
        stdin, lock_stdout, stderr = client.exec_command("gRPC")
        lock_stdout = lock_stdout.read().decode()
        # print(lock_stdout)
        locked = int(lock_stdout[-2])
        load(0.2)

    
    stdin, stdout, stderr = client.exec_command("gRPC")

    # Read and print the output
    esno = stdout.read().decode()
    # esno = stdout.read().decode()

    # Close the connection
    client.close()

    return esno