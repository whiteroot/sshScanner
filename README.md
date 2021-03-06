# SSH scanner

## Quickstart

This software requires python 3 and a linux box.

To install, setup and run the software:

    $ git clone https://github.com/whiteroot/sshScanner.git
    $ cd sshScanner
    $ python3 -m pip install -r requirements.txt

examples:

    $ ./scan_range.py --input credentials.txt --ports 22,8022,9022 --range 123.44.55.0/30 --output results.txt
    $ ./scan_range.py -i credentials.txt -p 22,8022,9022 -r 123.44.55.0/30 -o results.txt
    $ ./scan_range.py --users users.txt --passwords pass.txt --ports 22,8022,9022 --range 123.44.55.0/30 --output results.txt --workers 16
    $ ./scan_range.py -fu users.txt -fp pass.txt -p 22,8022,9022 -r 123.44.55.0/30 -o results.txt -w 16
    $ ./scan_range.py --users users.txt --passwords pass.txt --ports 22,8022,9022 --ip-port servers.txt --output results.txt --workers 16
