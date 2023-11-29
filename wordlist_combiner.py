# This script combines large files into a "master" file using hyperthreading and chunking to not crash with large files. 
# Usage: python3 wordlist_combiner.py <wordlist1> <wordlist2>
import argparse
from concurrent.futures import ThreadPoolExecutor

CHUNK_SIZE = 32768  # Adjust the chunk size based on your needs/RAM availability

def process_chunk(chunk):
    return set(chunk.splitlines())

def process_file(file):
    with open(file, "r", encoding="utf-8") as f:
        chunks = iter(lambda: f.read(CHUNK_SIZE), '')
        return set(entry for chunk in chunks for entry in process_chunk(chunk))

def combine_text_files(files):
    master_list = set()

    with ThreadPoolExecutor() as executor:
        file_contents = executor.map(process_file, files)
        master_list.update(entry for file_set in file_contents for entry in file_set)

    # Write the deduplicated entries to the master file
    with open("master.txt", "w", encoding="utf-8") as master_file:
        for entry in master_list:
            master_file.write(entry + '\n')

    print("Combining and deduplicating completed. Master list saved to master.txt.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine and deduplicate entries from text files into a master list.")
    parser.add_argument("files", nargs="+", help="List of text files to process")
    args = parser.parse_args()

    combine_text_files(args.files)
