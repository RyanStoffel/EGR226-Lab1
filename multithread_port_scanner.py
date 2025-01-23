from queue import Queue
import socket
import threading

# Global variables
target = input("Enter the target IP address: ")  # Replace with your target IP
queue = Queue()
open_ports = []

# Port scanning function
def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False

# Worker function for multithreading
def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print(f"Port {port} is open!")
            open_ports.append(port)

# Function to define ports for scanning
def get_ports(mode):
    if mode == 1:
        for port in range(1, 1024):  # Standard ports
            queue.put(port)
    elif mode == 2:
        for port in range(1, 49152):  # Reserved ports
            queue.put(port)
    elif mode == 3:
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]  # Critical ports
        for port in ports:
            queue.put(port)
    elif mode == 4:
        ports = input("Enter your ports (separate by space): ").split()
        ports = list(map(int, ports))
        for port in ports:
            queue.put(port)
    elif mode == 5:
        ports = [20, 21, 22, 23, 25, 53, 80, 88, 110, 123, 139, 143, 161, 162, 389, 443, 445, 465, 500, 636, 993, 1433, 1434, 3306, 5060, 5061, 8080]
        for port in ports:
            queue.put(port)


# Main function to run the scanner
def run_scanner(threads, mode):
    get_ports(mode)

    # Create worker threads
    thread_list = []
    for _ in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    # Start all threads
    for thread in thread_list:
        thread.start()

    # Wait for all threads to finish
    for thread in thread_list:
        thread.join()

    print("\nOpen ports are:", open_ports)

# Example usage
if __name__ == "__main__":
    print("Modes:")
    print("1 - Scan standard ports (1-1024)")
    print("2 - Scan reserved ports (1-49152)")
    print("3 - Scan critical ports only")
    print("4 - Custom port input")
    print("5 - Specific ports")
    mode = int(input("Select a mode: "))
    threads = int(input("Enter number of threads to use: "))

    run_scanner(threads, mode)
