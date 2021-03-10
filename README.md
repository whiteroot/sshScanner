# SSH scanner

## Quickstart

This software requires python 3.

To install, setup and run the software:

    $ git clone https://github.com/whiteroot/sshScanner.git
    $ cd sshScanner
    $ python3 -m pip install -r requirements.txt
    $ ./scan.py --file <file with IP|user|password> --ports <list of ports to scan>

examples:

    $ ./scan.py --file servers.txt --ports 22,8022,9022
    $ ./scan.py -f servers.txt -p 22,8022,9022
