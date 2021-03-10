# SSH scanner

## Quickstart

This software requires python 3.

To install, setup and run the software:

    $ git clone https://github.com/whiteroot/sshScanner.git
    $ cd sshScanner
    $ python3 -m pip install -r requirements.txt

examples:

    $ ./scan_from_file.py --file servers.txt --ports 22,8022,9022
    $ ./scan_from_file.py -f servers.txt -p 22,8022,9022
    $ ./scan_range.py --file credentials.txt --ports 22,8022,9022 --range 123.44.55.0/30
    $ ./scan_range.py -f credentials.txt -p 22,8022,9022 -r 123.44.55.0/30
