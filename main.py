#!/usr/bin/env python
from functools import partial
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy import and_, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

import hashlib
import multiprocessing
import os
import sys

import click


# Function that collects all files to count hashes
# If a file given as an argument, then add it to the list
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
def get_hash_alg(filename, alg):
    # Uncomment to see Processes starting counting hashes
    # print(
    #     'Counting hash for file: ' + filename + f' with process {multiprocessing.current_process().name} on'
    #                                             f' {time.ctime()}')
    with open(filename, "rb") as file:
        memory = hashlib.new(alg)
        while True:
            data = file.read()
            if not data:
                break
            memory.update(data)

        # Returns hashsum|filename values for each file
        # If algorithm name contains "shake" then limit number of letters in hash
        if "shake" in alg:
            return f"{memory.hexdigest(255)}|{filename}"
        else:

            return f"{memory.hexdigest()}|{filename}"


# Function for saving results to database
def save_func(response):
    for line in response:
        path_hash = line.split("|")
        query = session.query(Hash).filter(
            and_(Hash.path == path_hash[1], Hash.hash == path_hash[0])
        )

        # If entry with filename and its hash not in database then add it
        if not query.first():
            hashsum = Hash(path=path_hash[1], hash=path_hash[0])
            session.add(hashsum)
            session.commit()
        # If found file with different hashsum
        changed = 0
        exists = session.query(Hash).filter(
            and_(Hash.path == path_hash[1], Hash.hash != path_hash[0])
        )
        if exists.first():
            print(exists.first(), "changed to", path_hash[0])
            choice = input("Update hashsum? ")
            changed += 1
            # exit(0)
            # Delete old hashsum and add new one if entered "y" ("yes")
            if choice == "yes" or choice == "y":
                session.execute(delete(Hash).where(Hash.path == path_hash[1]))
                hashsum = Hash(path=path_hash[1], hash=path_hash[0])
                session.add(hashsum)
                session.commit()
    # #
    # if changed == 0:
    #     print("No changes detected")
    #     exit(0)


# Basic Click configuration
@click.command()
@click.option("--check", "-c", help="Read SHA sums from the FILEs and check them")
@click.option("--algorithm", "-a", help="Choose algorithm for hashing")
@click.option("--processes", "-p", type=int, help="Processes per core")
@click.option("--algorithms", "-al", is_flag=True, help="Display available algorithms")
def main(check, algorithm, processes, algorithms=True):
    """
    Checks if hashes for files changed o
    """
    # If -al parameter entered print all guaranteed algorithms
    if algorithms:
        for i in hashlib.algorithms_guaranteed:
            print(i)
        exit(0)
    # If algorithm is not set, then choose sha256 by default
    if not algorithm:
        algorithm = "sha256"
    elif not check:
        check = "./"

    # If string passed to script through the conveyor with or without algorithm set
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
                print(m.hexdigest(255))
            else:
                print(m.hexdigest())
        sys.stdin.close()
        exit(0)
    # If -p parameter for number of processes per core not set, then by default make it = 1
    if not processes:
        processes = 1

    # Mark start time of hashing process
    # Start hashing process for folder or file
    with multiprocessing.Pool(multiprocessing.cpu_count() * processes) as process:
        process.map_async(
            partial(get_hash_alg, alg=algorithm),
            find_all_files(check),
            callback=save_func,
        )
        process.close()
        process.join()


# Create ORM with sqlalchemy
Base: Any = declarative_base()
engine = create_engine("sqlite:///hashes.db", echo=False)
session = sessionmaker(bind=engine)()


# Class for ORM hash table
class Hash(Base):
    __tablename__ = "hashes"
    id = Column(Integer, primary_key=True)
    path = Column(String)
    hash = Column(String)

    # How the database object will be displayed
    def __repr__(self):
        return self.path


# If database doesn't exist, create it
if not os.path.isfile("hashes.db"):
    Base.metadata.create_all(engine)

# If called without parameters or "help" is passed

# if len(sys.argv) == 1 or sys.argv[1] == "help":
#     print("Usage: hashcli [path_to_file_or_folder] [algorithm] [processes_per_core]\n"
#           "Available algorithms: ")
#     for al in hashlib.algorithms_available:
#         print(al)
#
# if len(sys.argv) >= 2:
#     path = sys.argv[1] if len(sys.argv) > 1 else './'
#     algorithm = sys.argv[2] if len(sys.argv) > 2 else "sha256"
#     processes = int(sys.argv[3]) if len(sys.argv) > 3 else 5

if __name__ == "__main__":
    main()

    # print('Counting hashes in ' + path)
