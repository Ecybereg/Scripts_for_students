#!/usr/bin/env python

#© Copyright Erel Regev
#This script acts as LAN scanner for live hosts only.

from scapy.all import ARP, Ether, srp

target_ip = input("Enter the target IP range (e.g., 192.168.1.0/24): ")

arp = ARP(pdst=target_ip)
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
arp_request = ether/arp

result = srp(arp_request, timeout=3, verbose=False)[0]

print("Online hosts:")
for sent, received in result:
    print(received.psrc)
