#!/bin/bash

# Function to convert CIDR to range of IP addresses
cidr_to_ips() {
  local cidr=$1
  local ip mask
  local IFS='/'
  read -r ip mask <<< "$cidr"
  IFS=.

  read -r i1 i2 i3 i4 <<< "$ip"
  local ipnum=$(( (i1 << 24) + (i2 << 16) + (i3 << 8) + i4 ))
  local hostnum=$(( 1 << (32 - mask) ))
  local start_ip=$ipnum
  local end_ip=$(( ipnum + hostnum - 1 ))

  for ((i = start_ip; i <= end_ip; i++)); do
    echo "$(( (i >> 24) & 255 )).$(( (i >> 16) & 255 )).$(( (i >> 8) & 255 )).$(( i & 255 ))"
  done
}

# Check for proper usage
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <targets_file> <output_file>"
  exit 1
fi

TARGETS_FILE=$1
OUTPUT_FILE=$2
TARGETS_EXPANDED="targets_expanded.txt"

# Check if the targets file exists
if [ ! -f "$TARGETS_FILE" ]; then
  echo "Targets file not found: $TARGETS_FILE"
  exit 1
fi

# Create or clear the expanded targets file and output file
> "$TARGETS_EXPANDED"
> "$OUTPUT_FILE"

# Read IPs and CIDR ranges from targets file, expand CIDR ranges
while IFS= read -r target; do
  if [[ "$target" == *"/"* ]]; then
    cidr_to_ips "$target" >> "$TARGETS_EXPANDED"
  else
    echo "$target" >> "$TARGETS_EXPANDED"
  fi
done < "$TARGETS_FILE"

# Run the host command for each IP in expanded targets file and format the output
while IFS= read -r ip; do
  printf "\rRunning host command for IP: %s" "$ip"
  host_output=$(host "$ip")
  if [[ $? -eq 0 ]]; then
    host_name=$(echo "$host_output" | grep 'domain name pointer' | awk '{print $5}')
    if [ -n "$host_name" ]; then
      echo "$ip -- $host_name" >> "$OUTPUT_FILE"
    fi
  fi
done < "$TARGETS_EXPANDED"

# Clean up
rm "$TARGETS_EXPANDED"

# Clear the line after the loop
printf "\rAll IP addresses have been processed. Output is in %s\n" "$OUTPUT_FILE"
