# This script is used to listen for incoming ICMP packets and returns information on the IP that is sending the traffic. Great for testing command injection
import socket
import struct
import os
import sys

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except PermissionError:
        print("You need to run this script as an administrator or root.")
        sys.exit(1)

    print("Waiting for pings...")

    while True:
        packet, addr = sock.recvfrom(1024)
        print(f"Ping from: {addr[0]}")
        icmp_header = packet[20:28]
        icmp_type, icmp_code, icmp_checksum, icmp_packet_id, icmp_sequence = struct.unpack('bbHHh', icmp_header)

        print(f"ICMP Type: {icmp_type}")
        print(f"ICMP Code: {icmp_code}")
        print(f"ICMP Checksum: {icmp_checksum}")
        print(f"ICMP Packet ID: {icmp_packet_id}")
        print(f"ICMP Sequence: {icmp_sequence}")
        print("------------------------------------------------")

if __name__ == "__main__":
    main()
