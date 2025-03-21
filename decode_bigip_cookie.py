# This script is used to decode the IP address and port of BigIP servers using default settings that expose the encoded information in HTTP requests
import argparse
import socket

def decode_bigip_cookie(cookie):
    try:
        # Step 1: Split the cookie into its parts
        ip_part, port_part = cookie.split('.')
        print(f"\n[Step 1] Split Cookie:\n{cookie} → IP: {ip_part}, Port: {port_part}")

        # Step 2: Convert each part to hexadecimal
        ip_hex = format(int(ip_part), '08x')  # Ensure 8 characters (32-bit)
        port_hex = format(int(port_part), '04x')  # Ensure 4 characters (16-bit)
        print(f"\n[Step 2] Convert to Hex:\n{ip_part} → {ip_hex}\n{port_part} → {port_hex}")

        # Step 3: Reverse the byte order
        reversed_ip_hex = ''.join([ip_hex[i:i+2] for i in range(0, len(ip_hex), 2)][::-1])
        reversed_port_hex = ''.join([port_hex[i:i+2] for i in range(0, len(port_hex), 2)][::-1])
        print(f"\n[Step 3] Reverse Byte Order:\n{ip_hex} → {reversed_ip_hex}\n{port_hex} → {reversed_port_hex}")

        # Step 4: Convert reversed hex to decimal values
        ip_address = socket.inet_ntoa(bytes.fromhex(reversed_ip_hex))
        port_number = int(reversed_port_hex, 16)
        print(f"\n[Step 4] Convert Back to Decimal:\n{reversed_ip_hex} → {ip_address}\n{reversed_port_hex} → {port_number}")

        # Final decoded results
        print(f"\nDecoded IP Address: {ip_address}")
        print(f"Decoded Port Number: {port_number}")

    except Exception as e:
        print(f"\nError decoding cookie: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Decode F5 BIG-IP persistence cookies into IP address and port."
    )
    parser.add_argument(
        "cookie",
        help="BIG-IP persistence cookie string (e.g., 1677787402.47873)"
    )

    args = parser.parse_args()
    decode_bigip_cookie(args.cookie)

if __name__ == "__main__":
    main()
