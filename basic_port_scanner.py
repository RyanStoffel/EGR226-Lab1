import socket

def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", port))
        return True
    except:
        return False

# Testing for port 22
print(portscan(22)) # Will print True if port 22 is open, otherwise False

for port in range(1, 1024):
    result = portscan(port)

    if result:
        print("Port {} is open!".format(port))
    else:
        print("Port {} is closed!".format(port))


