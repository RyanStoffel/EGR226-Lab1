import scapy.all as scapy
import argparse


# Function to parse command-line arguments
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='Target IP Address/Addresses')
    options = parser.parse_args()

    # Check for errors if the user does not specify the target IP Address
    if not options.target:
        parser.error("[-] Please specify an IP Address or Addresses, use --help for more info.")
    return options


# Function to perform ARP scan
def scan(ip):
    # Create ARP request and broadcast frame
    arp_req_frame = scapy.ARP(pdst=ip)
    broadcast_ether_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame

    # Send the packet and collect responses
    answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout=1, verbose=False)[0]
    result = []

    # Process the responses
    for i in range(len(answered_list)):
        client_dict = {"ip": answered_list[i][1].psrc, "mac": answered_list[i][1].hwsrc}
        result.append(client_dict)
    return result


# Function to display the results
def display_result(result):
    print("-----------------------------------")
    print("IP Address\tMAC Address")
    print("-----------------------------------")
    for i in result:
        print("{}\t{}".format(i["ip"], i["mac"]))


# Main script execution
if __name__ == "__main__":
    options = get_args()  # Get user-provided arguments
    scanned_output = scan(options.target)  # Scan the target
    display_result(scanned_output)  # Display the results