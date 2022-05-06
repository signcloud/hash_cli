**Installation**:

**Step 1:**
ln -s /absolute/path/to/hash.py /usr/bin/hashcli

**Step 2:** 
Run "chmod +x hash.py" to be able to run script like ./main.py

**Step 3:**
hashcli [path] -a [algorithm] -c [file_to_read_or_write] -p [processes_per_core] -w

or just

hashcli --help in order to get help

**Example:**
hashcli ./ -a sha256 -p 5 -c hashes -w

 **This will run script for folder "./" (can be provided path to file), hashing algorithm sha256 and 5 processes per CPU core**
**-c parameter says to what file to write to or read from results**
**-w option says to write results to file**
 
 **Number of processes  per core and algorithm is optional parameters**

To run tests type:

pytest -v
