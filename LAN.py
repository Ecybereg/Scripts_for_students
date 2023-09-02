#!/usr/bin/env python

#© Copyright Erel Regev
#This script acts as LAN scanner for live hosts only.


from scapy.all import ARP, Ether, srp

# Prompt the user for the target IP range
target_ip = input("Enter the target IP range (e.g., 192.168.1.0/24): ")

# Create an ARP request packet
arp = ARP(pdst=target_ip)
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
arp_request = ether/arp

# Send the packet and receive responses
result = srp(arp_request, timeout=3, verbose=False)[0]

# Print the IP addresses of online hosts
print("Online hosts:")
for sent, received in result:
    print(received.psrc)
