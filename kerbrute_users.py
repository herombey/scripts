# Usage = python3 kerbrute_users.py <kerbrute file.txt>
import re
import sys

if len(sys.argv) < 2:
    print("Please provide the input file name as a command argument")
    sys.exit(1)

input_file_name = sys.argv[1]
pattern = r"VALID USERNAME:\s+(\w+)"

with open(input_file_name, "r") as input_file:
    with open("users.txt", "w") as output_file:
        unique_usernames = set()
        for line in input_file:
            match = re.search(pattern, line)
            if match:
                username = match.group(1)
                lowercase_username = username.lower()
                if lowercase_username not in unique_usernames:
                    output_file.write(username + "\n")
                    unique_usernames.add(lowercase_username)
