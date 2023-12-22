# This script is used to read Hack the Box Academy Cheatsheets in .md and extract the command and description into code blocks for markdown note apps like Obsidian.
# Usage: python3 command_splitter.py <inputfile.md> <outputfile.md>
import sys
import re

def process_markdown_table(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Check if line contains a table row with a command
            if '|' in line and '`' in line:
                # Extract the command and description
                match = re.search(r'\|\s*`([^`]+)`\s*\|\s*([^|]+)\s*\|', line)
                if match:
                    command = match.group(1)
                    description = match.group(2).strip()

                    # Write to output file
                    outfile.write(f"{description}\n")
                    outfile.write("```bash\n")
                    outfile.write(f"{command}\n")
                    outfile.write("```\n\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    # Check if the input file exists
    try:
        process_markdown_table(input_file_path, output_file_path)
    except FileNotFoundError:
        print("Error: Input file does not exist.")
        sys.exit(1)
