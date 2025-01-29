#!/usr/bin/env python3

#© Copyright Erel Regev
#This script extracts information from a PCAP file such as IPs list, MAC list, Hostnames, User-agents.

import os
import sys
from scapy.all import rdpcap, Ether, IP, ARP, TCP, UDP
from socket import gethostbyaddr

def extract_unique_values(pcap_file):
    packets = rdpcap(pcap_file)
    
    ipv4_addresses = set()
    ipv6_addresses = set()
    mac_addresses = set()
    protocols = set()
    hostnames = {}
    user_agents = set()

    total_packets = len(packets)
    current_packet = 0

    for packet in packets:
        current_packet += 1
        print(f"Analyzing packet {current_packet}/{total_packets}", end="\r")

        if Ether in packet:
            mac_addresses.add(packet[Ether].src)
            mac_addresses.add(packet[Ether].dst)

        if IP in packet:
            ipv4_addresses.add(packet[IP].src)
            ipv4_addresses.add(packet[IP].dst)
            protocol_name = get_protocol_name(packet[IP].proto)
            protocols.add(protocol_name)
            
            try:
                hostname = gethostbyaddr(packet[IP].src)[0]
                add_to_hostnames(hostnames, protocol_name, packet[IP].src, hostname)
            except:
                pass
            
            try:
                hostname = gethostbyaddr(packet[IP].dst)[0]
                add_to_hostnames(hostnames, protocol_name, packet[IP].dst, hostname)
            except:
                pass

        if TCP in packet and packet[TCP].dport == 80 and 'User-Agent' in str(packet):
            user_agent = str(packet[packet[TCP].payload].load).split('\n')[0]
            user_agents.add(user_agent)
    
    if not os.path.exists("analyzer"):
        os.makedirs("analyzer")
    
    save_to_file("analyzer/ipv4_addresses.txt", ipv4_addresses)
    save_to_file("analyzer/ipv6_addresses.txt", ipv6_addresses)
    save_to_file("analyzer/mac_addresses.txt", mac_addresses)
    save_to_file("analyzer/protocols.txt", protocols)
    save_to_file_with_titles("analyzer/hostnames.txt", hostnames)
    save_to_file("analyzer/user_agents.txt", user_agents)

def save_to_file(file_path, data):
    with open(file_path, "w") as f:
        for item in data:
            f.write(str(item) + "\n")

def save_to_file_with_titles(file_path, data):
    with open(file_path, "w") as f:
        for protocol, hosts in data.items():
            f.write(f"Protocol: {protocol}\n")
            for host, hostname in hosts.items():
                f.write(f"IP: {host}, Hostname: {hostname}\n")
            f.write("\n")

def add_to_hostnames(hostnames, protocol, ip, hostname):
    if protocol not in hostnames:
        hostnames[protocol] = {}
    hostnames[protocol][ip] = hostname

def get_protocol_name(proto_number):
    protocol_names = {
        1: "ICMP",
        6: "TCP",
        17: "UDP"
    }
    return protocol_names.get(proto_number, str(proto_number))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <pcap_file>".format(sys.argv[0]))
        sys.exit(1)

    pcap_file = sys.argv[1]
    extract_unique_values(pcap_file)
    print("\nAnalysis complete!")
