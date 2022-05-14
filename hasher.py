#!/usr/bin/env python
from functools import partial

import hashlib
import multiprocessing
import os

# import time
import sys

import click

import logging

logging.basicConfig(format="%(message)s", level=logging.DEBUG)
logger = logging.getLogger()


class HashFiles:
    def __init__(self, root_path, algorithm, processes):
        self.root_path = root_path
        if not algorithm:
            self.algorithm = "sha256"
        self.algorithm = algorithm
        self.processes = processes

    def find_all_files_and_check(self):
        # self.root_path = root_path
        files_list = []
        # If argument is file then add it to the list
        if os.path.isfile(self.root_path):
            print("File found", self.root_path)
            files_list.append(self.root_path)
        # Walk through all the folders in path and append all the files to the list
        for root, _, files in os.walk(self.root_path, topdown=True):
            for name in files:
                filepath = os.path.join(root, name)
                if os.path.exists(filepath):
                    files_list.append(filepath)

        for file in files_list:
            self.hash_multiprocessing(file)

    def get_hash_algorithm(self, file):
        with open(file, "rb") as file:
            memory = hashlib.new(self.algorithm)
            while True:
                data = file.read()
                if not data:
                    break
                memory.update(data)

            # Returns hashsum|filename values for each file
            # If algorithm name contains "shake" then limit number of letters in
            # hash
            if "shake" in self.algorithm:
                return f"{memory.hexdigest(255)}  {file}"
            else:
                return f"{memory.hexdigest()}  {file}"

    def save(self, response, file="", force=False):
        print("Save")
        if not file:
            for line in response:
                logger.info(line)
        # If -c filename is given and got response
        # If function is called with filepath argument and got response from multiprocessing
        elif file and not os.path.isdir(file) and response:
            # Write to file if file doesn't exist or function called with force parameter set to True
            if not os.path.exists(file) or force:
                with open(file, "w") as file:
                    for line in response:
                        file.write(line + "\n")
            else:
                logger.info("File already exists")
                rewrite = input("Do you want to rewrite it? ")
                if rewrite == "yes" or rewrite == "y":
                    self.save(response, file, force=True)

    def hash_multiprocessing(self, file: str) -> None:
        with multiprocessing.Pool(multiprocessing.cpu_count() * self.processes) as process:
            process.apply_async(
                partial(self.get_hash_algorithm, alg=self.algorithm),
                file,
                callback=partial(self.save, file=file),
            )
            process.close()
            process.join()

    def check_file(self, file=""):
        unmatched = []
        with open(file, "r") as file:
            for line in file:
                hash_file = line.strip().split("  ")
                # Count hash for file and check if it changed
                if self.get_hash_algorithm(hash_file[1].strip()) in line:
                    logger.info(f"{hash_file[1]}: OK")
                else:
                    unmatched.append(hash_file[1])
                    logger.info(f"{hash_file[1]}: FAILED")
            count_unmatched = len(unmatched)
            if count_unmatched > 0:
                logger.info(
                    f"{os.path.basename(__file__)}: WARNING: {count_unmatched} computed checksums did NOT match:"
                )
                for i in unmatched:
                    logger.info(i)
                exit(1)


@click.command()
@click.argument("file", required=False, type=click.Path(exists=True))
@click.option("--check", "-c", help="Read SHA sums from the FILEs and check them or write to file if file (or folder) "
                                    "argument is given")
@click.option("--algorithm", "-a", help="Choose algorithm for hashing")
@click.option("--processes", "-p", type=int, help="Processes per core")
@click.option("--algorithms", "-al", is_flag=True, help="Display available algorithms")
def main(file, check, algorithm, processes, algorithms=True):
    """
    Checks if hashes for files changed or not. By default uses sha256 algorithm.
    """
    # If -al option is set, print all guaranteed algorithms
    if algorithms:
        for i in hashlib.algorithms_available:
            logger.info(i)
        exit(0)
    # If algorithm is not set, then choose sha256 by default
    if not algorithm:
        algorithm = "sha256"

    if check and not file:
        if os.path.exists(check):
            check_file = HashFiles(file, algorithm, processes)
            check_file.check_file(file=check, algorithm=algorithm)
        exit(0)

    # If string passed to script through the conveyor with or without
    # algorithm set
    if (
            check != "./"
            and len(sys.argv) == 1
            or len(sys.argv) == 3
            and algorithm in sys.argv
    ):
        for line in sys.stdin:
            b = line.encode()
            m = hashlib.new(algorithm)
            m.update(b)
            # If using shake_* algorithm then limit number of letters in hash
            if "shake" in algorithm:
                logger.info(m.hexdigest(255))
            else:
                logger.info(m.hexdigest())
        sys.stdin.close()
        exit(0)
    # If -p parameter for number of processes per core not set, then by
    # default make it = 1
    if not processes:
        processes = 1

    # Mark start time of hashing process
    # st_time = time.time()
    # Start hashing process for folder or file
    hashfile = HashFiles(file, algorithm, processes)
    hashfile.find_all_files_and_check()
    # end_time = time.time()
    # Count time spent hashing folder
    # diff_time = end_time - st_time
    # Uncomment the line below to display the time taken to calculate
    # print(diff_time, 'Processes/CPU core:', processes, 'CPU cores:', multiprocessing.cpu_count())


if __name__ == "__main__":
    main()
