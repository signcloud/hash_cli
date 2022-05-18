**Installation**:

**Step 1:**
ln -s /absolute/path/to/sha.py /usr/bin/hashcli

**Step 2:**
Run "chmod +x sha.py" to be able to run script like hashcli

**Step 3:**
hashcli [path] -a [algorithm] -c [file_to_read_or_write] -p [processes_per_core]

or just

hashcli --help in order to get help

**Example:**
hashcli ./ -a sha256 -p 5 -c hashes

**This will run script for folder "./" (can be provided path to file), hashing algorithm sha256 and 5 processes per CPU core**
**and will save results to file "hashes"**
**-c parameter says to what file to write to or read from results**

 **Number of processes per core and algorithm are optional parameters**

To run tests type:

pytest -v

**To install Docker containter type:**

docker build -t hashcli .

Then enter in order to get help:

docker run hashcli --help

Run:
docker run -v /home/dzhdanov@scnsoft.com/Projects/hash:/usr/app/src/dir hashcli ./dir/test

=======
Run: docker run -v /home/dzhdanov@scnsoft.com/Projects/hash:/usr/app/src/dir hashcli ./dir/test
