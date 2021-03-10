# SSH scanner

## Quickstart

This software requires python 2.

To install, setup and run the software:

    $ git clone https://github.com/whiteroot/sshScanner.git
    $ cd sshScanner
    $ python2 -m pip install -r requirements.txt
    $ ./scan.py --file <file with IP|user|password> --ports <list of ports to scan>
    $ example:
    $ ./scan.py --file servers.txt --ports 22,8022,9022
