#!/usr/bin/env python
import time
import hashlib
import multiprocessing
import os
import sys
import threading
# from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool as ThreadPool

from functools import partial

import click

import logging

debug = False


logging.basicConfig(format="%(message)s", level=logging.DEBUG)
logger = logging.getLogger()


class HashFiles:
    def __init__(self, root_path, check, algorithm, processes=1):
        self.check = check
        self.root_path = root_path
        self.algorithm = algorithm
        self.processes = processes
        self.result = []

        if self.algorithm.isnumeric():
            self.algorithm = "sha" + self.algorithm

        if self.algorithm not in hashlib.algorithms_available:
            logger.info("Wrong algorithm")

        if not processes:
            self.processes = 1
        if self.root_path:
            self.hash_multiprocessing()

    def get_hash_algorithm(self, file):
        if debug:
            if multiprocessing.current_process().name == "MainProcess":
                print(f'Counting hash for file: {file} with thread {threading.current_thread().name} on {time.ctime()}')
            else:
                print(
                    f'Counting hash for file: {file} with process {multiprocessing.current_process().name} on {time.ctime()}')

        with open(file, "rb") as hash_file:
            mem = hashlib.new(self.algorithm)
            while True:
                contents = hash_file.read(1024)
                if not contents:
                    break
                mem.update(contents)

        if "shake" in self.algorithm:
            return f"{mem.hexdigest(255)}  {file}"
        else:
            return f"{mem.hexdigest()}  {file}"

    def find_files(self):
        files_list = []
        # If argument is file then add it to the list
        if os.path.isfile(self.root_path):
            files_list.append(self.root_path)
        # Walk through all the folders in path and append all the files to the list
        for root, _, files in os.walk(self.root_path, topdown=True):
            for name in files:
                filepath = os.path.join(root, name)
                if os.path.exists(filepath):
                    files_list.append(filepath)
        return files_list

    def hash_multiprocessing(self):
        with ThreadPool(
                multiprocessing.cpu_count() * self.processes
        ) as process:
            process.map_async(
                self.get_hash_algorithm,
                self.find_files(),
                callback=partial(self.save_hashes, check=self.check),
            )
            process.close()
            process.join()
        return process

    def save_hashes(self, response, check="", force=False):
        if not check:
            for line in response:
                logger.info(line)
            # If -c filename is given and got response
            # If function is called with filepath argument and got response from multiprocessing
        elif check and not os.path.isdir(check) and response:
            # Write to file if file doesn't exist or function called with force parameter set to True
            if not os.path.exists(check) or force:
                with open(check, "w") as file:
                    for line in response:
                        file.write(line + "\n")
            else:
                logger.info("File already exists")
                rewrite = input("Do you want to rewrite it? ")
                if rewrite == "yes" or rewrite == "y":
                    self.save_hashes(response=response, check=check, force=True)
        else:
            logger.info(check + " is a directory")
        return response

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

            return unmatched

    def __str__(self):
        return str(self.result)


@click.command()
@click.argument("file", required=False, type=click.Path(exists=True))
@click.option(
    "--check",
    "-c",
    help="Read SHA sums from the FILEs and check them or write to file if file (or folder) "
         "argument is given",
)
@click.option("--algorithm", "-a", help="Choose algorithm for hashing")
@click.option("--processes", "-p", type=int, help="Processes per core")
@click.option("--algorithms", "-al", is_flag=True, help="Display available algorithms")
def main(file, check, algorithm, processes, algorithms=True):
    """
    Checks if hashes for files changed or not. By default, uses sha256 algorithm.
    """
    start_time = time.time()
    if algorithms:
        for i in hashlib.algorithms_available:
            logger.info(i)
        exit(0)

    if not algorithm:
        algorithm = "sha256"

    if len(sys.argv) == 1 or len(sys.argv) == 3 and algorithm in sys.argv:
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

    unmatched = []
    if check and not file:
        if os.path.exists(check):
            check_file = HashFiles(file, check, algorithm, processes)
            unmatched = check_file.check_file(file=check)

    HashFiles(file, check, algorithm, processes)
    end_time = time.time()
    diff_time = end_time - start_time
    logger.info("Time spent counting: " + str(diff_time))

    if len(unmatched) > 0:
        exit(1)


if __name__ == "__main__":
    main()
