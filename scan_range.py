#!/usr/bin/env python3

import sys
from ipaddress import ip_address, ip_network

import helper


def get_creds(f):
    with open(f, 'r') as f:
        for line in f:
            x = line.split('|')
            yield x[0], x[1].strip()

def get_ip(cidr):
    net = ip_network(cidr, strict=False)
    for ip in net:
        yield ip


def main(argv):
    _file = None
    ip_range = None
    ports = [22]  # default port list
    argc = len(sys.argv)
    i = 1
    while (i < argc):
        if sys.argv[i] in ('-f', '--file'):
            _file = sys.argv[i+1]
            i += 2
        elif sys.argv[i] in ('-p', '--port', '--ports'):
            ports = [int(p) for p in sys.argv[i+1].split(',')]
            i += 2
        elif sys.argv[i] in ('-r', '--range'):
            ip_range = sys.argv[i+1]
            i += 2
        else:
            print('Unknown arg: {sys.argv[i]}')
            sys.exit(1)

    if not (_file and ip_range):
        print('Missing arg')
        sys.exit(1)

    for proxy in get_ip(ip_range):
        for user, password in get_creds(_file):
            for port in ports:
                try:
                    ret = helper.try_login(proxy, port, user, password)
                    if ret:
                        print("{}:{}@{}:{} OK".format(user, password, proxy, port))
                        break
                    else:
                        print("{}:{}@{}:{} ko".format(user, password, proxy, port))
                except Exception as e:
                    print("{}:{}@{}:{} ko".format(user, password, proxy, port))


if __name__ == '__main__':
    main(sys.argv)
