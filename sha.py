#!/usr/bin/env python
from functools import partial

import hashlib
import multiprocessing
import os
import sys

import click

import logging

logging.basicConfig(format="%(message)s", level=logging.DEBUG)
logger = logging.getLogger()


class HashFiles:
    def __init__(self, root_path, algorithm, processes):
        self.result = ""
        self.root_path = root_path
        self.algorithm = algorithm
        if not algorithm:
            self.algorithm = "sha256"
        self.processes = processes if processes else 1

        if root_path:
            if os.path.isdir(root_path):
                self.hash_dir(root_path)
            elif os.path.isfile(root_path):
                self.hash_file()

    def get_hash_algorithm(self, file):
        with open(file, "rb") as hash:
            memory = hashlib.new(self.algorithm)
            while True:
                data = hash.read()
                if not data:
                    break
                memory.update(data)

        if "shake" in self.algorithm:
            return f"{memory.hexdigest(255)}  {file}"
        else:
            return f"{memory.hexdigest()}  {file}"

    def hash_multiprocessing(self, file: str):
        with multiprocessing.Pool(
                multiprocessing.cpu_count() * self.processes
        ) as process:
            process.apply_async(self.get_hash_algorithm, (file,), callback=self.save)
            process.close()
            process.join()

    def hash_file(self):
        self.hash_multiprocessing(self.root_path)

    def hash_dir(self, dirname):
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

        for file in files_list:
            hash_file = HashFiles(file, self.algorithm, self.processes)
            self.result += str(hash_file) + "\n"

    def save(self, response):
        self.result += response

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

    def __str__(self):
        return self.result.strip()


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
    if algorithms:
        for i in hashlib.algorithms_available:
            logger.info(i)
        exit(0)

    if not algorithm:
        algorithm = "sha256"

    if (len(sys.argv) == 1
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

    if check and not file:
        # print(check)
        if os.path.exists(check):
            check_file = HashFiles(file, algorithm, processes)
            check_file.check_file(file=check)
        exit(0)

    hashfile = HashFiles(file, algorithm, processes)

    print(hashfile)


if __name__ == "__main__":
    main()
