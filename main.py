#!/usr/bin/env python
from functools import partial

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy import and_, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

import hashlib
import multiprocessing
import os
import time
import sys

Base = declarative_base()
engine = create_engine('sqlite:///hashes.db', echo=False)
session = sessionmaker(bind=engine)()


class Hash(Base):
    __tablename__ = 'hashes'
    id = Column(Integer, primary_key=True)
    path = Column(String)
    hash = Column(String)

    def __repr__(self):
        return self.path


def find_all_files(root_path):
    files_list = []
    if os.path.isfile(root_path):
        files_list.append(root_path)

    for root, dirs, files in os.walk(root_path, topdown=True):
        for name in files:
            filepath = os.path.join(root, name)
            if os.path.exists(filepath):
                files_list.append(filepath)
    return files_list


# Dictionary with available algorithms and its handlers
algorithms = {'sha3_512': hashlib.sha3_512,
              'sha1': hashlib.sha1,
              'sha512': hashlib.sha512,
              # 'shake_128': hashlib.shake_128,
              'sha3_224': hashlib.sha3_224,
              'sha256': hashlib.sha256,
              'sha3_256': hashlib.sha3_256,
              'shake_256': hashlib.shake_256,
              'blake2b': hashlib.blake2b,
              'blake2s': hashlib.blake2s,
              'md5': hashlib.md5}


def get_hash_alg(filename, alg):
    # Uncomment to see Processes starting counting hashes
    # print(
    #     'Counting hash for file: ' + filename + f' with process {multiprocessing.current_process().name} on'
    #                                             f' {time.ctime()}')
    with open(filename, 'rb') as f:
        m = algorithms[alg]()
        while True:
            data = f.read()
            if not data:
                break
            m.update(data)
        return f'{m.hexdigest()}|{filename}'


def save_func(response):
    for line in response:
        path_hash = line.split("|")
        query = session.query(Hash).filter(and_(Hash.path == path_hash[1], Hash.hash == path_hash[0]))
        if not query.first():
            hashsum = Hash(path=path_hash[1], hash=path_hash[0])
            session.add(hashsum)
            session.commit()
            # If found file with different hashsum
        exists = session.query(Hash).filter(and_(Hash.path == path_hash[1], Hash.hash != path_hash[0]))
        if exists.first():
            print(exists.first(), "changed to", path_hash[0])
            choice = input("Update hashsum? ")

            # Delete old hashsum and add new one if entered "y" ("yes")
            if choice == "yes" or choice == "y":
                session.execute(delete(Hash).where(Hash.path == path_hash[1]))
                hashsum = Hash(path=path_hash[1], hash=path_hash[0])
                session.add(hashsum)
                session.commit()


# If called without parameters or "help" is passed
if len(sys.argv) == 1 or sys.argv[1] == "help":
    print("Usage: python3 main.py [path_to_file_or_folder] [algorithm] [processes_per_core]\n"
          "Available algorithms: ")
    for al in algorithms:
        print(al)

if len(sys.argv) >= 3:
    path = sys.argv[1] if len(sys.argv) > 1 else './'
    algorithm = sys.argv[2]
    processes = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    if __name__ == '__main__':
        # print('Counting hashes in ' + path)
        st_time = time.time()
        with multiprocessing.Pool(multiprocessing.cpu_count() * processes) as p:
            p.map_async(partial(get_hash_alg, alg=algorithm), find_all_files(path), callback=save_func)
            p.close()
            p.join()  #
        end_time = time.time()
        diff_time = end_time - st_time
        # Uncomment the line below to display the time taken to calculate
        # print(diff_time, 'Processes/CPU core:', processes, 'CPU cores:', multiprocessing.cpu_count())
