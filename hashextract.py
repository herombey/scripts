# Usage = `python3 hashextract.py lsadump.txt`
import re
from collections import Counter
import sys

if len(sys.argv) != 2:
    print("Usage: python script.py input_file")
    sys.exit(1)

filename = sys.argv[1]
output_filename = "lsadumphash.txt"

username_regex = r"Username: (\S+)"
nt_regex = r"NT: (\S+)"

usernames = []
nt_hashes = []

with open(filename, "r") as f:
    content = f.read()
    usernames = re.findall(username_regex, content)
    nt_hashes = re.findall(nt_regex, content)

username_nt_list = [f"{user}:{nt}" for user, nt in zip(usernames, nt_hashes)]

with open(output_filename, "w") as f:
    f.write("\n".join(username_nt_list))

duplicates = [f"{user}={count}" for user, count in Counter(username_nt_list).items() if count > 1]

if duplicates:
    print("The following usernames and NT hashes are duplicated:")
    for dup in duplicates:
        print(dup)
