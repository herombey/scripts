# Usage = python passgen.py P@ssw0rd
import argparse
import re

def generate_leet_passwords(password):
    replacements = {
        "a": "4",
        "e": "3",
        "i": "1",
        "o": "0",
        "s": "5",
        "t": "7"
    }

    passwords = set()
    for c in password:
        if c.lower() in replacements:
            for r in replacements[c.lower()]:
                new_password = password.replace(c, r)
                passwords.add(new_password)
    return passwords

def generate_number_passwords(password):
    passwords = set()
    for i in range(100):
        new_password = password + str(i)
        passwords.add(new_password)
    return passwords

def generate_changed_number_passwords(password):
    replacements = {
        "0": "9",
        "1": "2",
        "2": "3",
        "3": "4",
        "4": "5",
        "5": "6",
        "6": "7",
        "7": "8",
        "8": "9",
        "9": "0"
    }
    
    passwords = set()
    for c in password:
        if c.isdigit():
            for r in replacements[c]:
                new_password = password.replace(c, r)
                passwords.add(new_password)
    return passwords

def generate_changed_capitalization_passwords(password):
    passwords = set()
    for i in range(2**len(password)):
        new_password = ""
        for j in range(len(password)):
            if i & (1<<j):
                new_password += password[j].upper()
            else:
                new_password += password[j].lower()
        passwords.add(new_password)
    return passwords

parser = argparse.ArgumentParser()
parser.add_argument("password", help="the sample password to generate similar passwords from")
args = parser.parse_args()

similar_passwords = set()
password = args.password

similar_passwords.update(generate_leet_passwords(password))

similar_passwords.update(generate_number_passwords(password))

similar_passwords.update(generate_changed_number_passwords(password))

similar_passwords.update(generate_changed_capitalization_passwords(password))

with open("similar_passwords.txt", "w") as output_file:
    for password in similar_passwords:
        output_file.write(password + "\n")
