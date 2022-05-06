#!/usr/bin/env python
from functools import partial

import hashlib
import multiprocessing
import os
import time
import sys

import click


# Function that collects all files in folder
# If a file given as an argument then add it to the list
def find_all_files(root_path):
    files_list = []
    # If argument is file then add it to the list
    if os.path.isfile(root_path):
        files_list.append(root_path)
    # Walk through all the folders in path and append all the files to the list
    for root, dirs, files in os.walk(root_path, topdown=True):
        for name in files:
            filepath = os.path.join(root, name)
            if os.path.exists(filepath):
                files_list.append(filepath)
    return files_list


# Multiprocess function than counts hashes for files
# Read file and hash its data with given algorithm
def get_hash_alg(filename, alg):
    # Uncomment to see Processes starting counting hashes
    # print(
    #     'Counting hash for file: ' + filename + f' with process {multiprocessing.current_process().name} on'
    #                                             f' {time.ctime()}')
    with open(filename, 'rb') as file:
        memory = hashlib.new(alg)
        while True:
            data = file.read()
            if not data:
                break
            memory.update(data)

        # Returns hashsum|filename values for each file
        # If algorithm name contains "shake" then limit number of letters in
        # hash
        if "shake" in alg:
            return f'{memory.hexdigest(255)}  {filename}'
        else:
            return f'{memory.hexdigest()}  {filename}'


# Function for saving results to file, checking if hashes changed
# according to those in file
def save_check_func(response="", file="", algorithm="sha256"):
    # If -c parameter not set then just print the result
    if not file:
        for line in response:
            print(line)
    # If -c filename is given and got response
    elif file and not os.path.isdir(file) and response:
        if os.path.exists(file):
            rewrite = input(f"File \"{file}\" already exists, rewrite file? (yes|no) ")
        if rewrite == "yes" or rewrite == "y":
            with open(file, "w") as file:
                for line in response:
                    file.write(line + "\n")
    # If function is called with filepath argument and got response from
    # multiprocessing
    elif not response:
        unmatched = []
        with open(file, "r") as file:
            for line in file:
                hash_file = line.strip().split("  ")
                # Count hash for file and check if it changed
                if get_hash_alg(hash_file[1].strip(), algorithm) in line:
                    print(f"{hash_file[1]}:", "OK")
                else:
                    unmatched.append(hash_file[1])
                    print(f"{hash_file[1]}:", "FAILED")
            if len(unmatched) > 0:
                print(
                    f"{os.path.basename(__file__)}: WARNING: {len(unmatched)} computed checksums did NOT match:")
                for i in unmatched:
                    print(i)
                exit(1)
    else:
        print(file, "is a directory")


@click.command()
@click.argument("file", required=False, type=click.Path(exists=True))
@click.option("--check", "-c",
              help="Read SHA sums from the FILEs and check them")
@click.option("--algorithm", "-a", help="Choose algorithm for hashing")
@click.option("--processes", "-p", type=int, help="Processes per core")
@click.option("--write", "-w", is_flag=True, help="Save results to file")
@click.option("--algorithms", "-al", is_flag=True,
              help="Display available algorithms")
def main(write, file, check, algorithm, processes, algorithms=True):
    """
    Checks if hashes for files changed or not
    """
    # If -al option is set, print all guaranteed algorithms
    if algorithms:
        for i in hashlib.algorithms_guaranteed:
            print(i)
        diff = hashlib.algorithms_available - hashlib.algorithms_guaranteed
        print("ADD:", diff)
        exit(0)
    # If algorithm is not set, then choose sha256 by default
    if not algorithm:
        algorithm = "sha256"

    if check and not file:
        if os.path.exists(check):
            save_check_func(file=check, algorithm=algorithm)
        exit(0)

    # If string passed to script through the conveyor with or without
    # algorithm set
    if check != "./" and len(
            sys.argv) == 1 or len(sys.argv) == 3 and algorithm in sys.argv:
        for line in sys.stdin:
            b = line.encode()
            m = hashlib.new(algorithm)
            m.update(b)
            # If using shake_* algorithm then limit number of letters in hash
            if "shake" in algorithm:
                print(m.hexdigest(255))
            else:
                print(m.hexdigest())
        sys.stdin.close()
        exit(0)
    # If -p parameter for number of processes per core not set, then by
    # default make it = 1
    if not processes:
        processes = 1

    # Mark start time of hashing process
    st_time = time.time()
    # Start hashing process for folder or file
    with multiprocessing.Pool(multiprocessing.cpu_count() * processes) as process:
        process.map_async(
            partial(
                get_hash_alg,
                alg=algorithm),
            find_all_files(file),
            callback=partial(
                save_check_func,
                file=check))
        process.close()
        process.join()
    end_time = time.time()
    # Count time spent hashing folder
    diff_time = end_time - st_time
    # Uncomment the line below to display the time taken to calculate
    # print(diff_time, 'Processes/CPU core:', processes, 'CPU cores:', multiprocessing.cpu_count())


if __name__ == '__main__':
    main()
