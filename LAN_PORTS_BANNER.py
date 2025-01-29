#!/usr/bin/env python

#© Copyright Erel Regev
#This script acts as LAN scanner for live hosts, and extracts open ports and versions of the services running on the found ports.

import socket
from scapy.all import ARP, Ether, srp

def scan_lan(target_ip):
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request = ether/arp
    
    result = srp(arp_request, timeout=3, verbose=False)[0]
    
    live_hosts = [received.psrc for sent, received in result]
    return live_hosts

def scan_ports(host, ports):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        
        result = sock.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

def get_service_version(host, port):
    banner = ""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.settimeout(2)
            
            banner = s.recv(1024).decode().strip()
    except Exception as e:
        pass
    return banner

def main():
    target_ip = input("Enter the target IP range (e.g., 192.168.1.0/24): ")
    live_hosts = scan_lan(target_ip)
    
    ports_option = input("Enter the ports to scan (e.g., 80, 443, 8080-8090, all): ")
    if ports_option == "all":
        ports = range(1, 65536)
    else:
        ports = []
        port_ranges = ports_option.split(",")
        for prange in port_ranges:
            if "-" in prange:
                start, end = prange.split("-")
                ports.extend(range(int(start), int(end) + 1))
            else:
                ports.append(int(prange))
    
    for host in live_hosts:
        print(f"Scanning {host}...")
        open_ports = scan_ports(host, ports)
        
        if open_ports:
            print(f"Open ports on {host}: {open_ports}")
            for port in open_ports:
                service_banner = get_service_version(host, port)
                if service_banner:
                    print(f"Service on port {port}: {service_banner}")
                else:
                    print(f"Port {port} does not provide a service banner")
        else:
            print(f"No open ports found on {host}")

if __name__ == "__main__":
    main()
