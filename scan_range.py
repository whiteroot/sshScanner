#!/usr/bin/env python3

import sys
from ipaddress import ip_network

import helper
from constants import cx_status


def get_creds(f):
    with open(f, 'r') as f:
        for line in f:
            x = line.split('|')
            yield x[0], x[1].strip()


def get_ip(cidr):
    net = ip_network(cidr, strict=False)
    for ip in net:
        yield str(ip)


def main(argv):
    in_file = None
    out_file = '/tmp/ssh_scan_results.txt'
    ip_range = None
    verbose = True
    ports = [22]  # default port list
    argc = len(sys.argv)
    i = 1
    while (i < argc):
        if sys.argv[i] in ('-i', '--input'):
            in_file = sys.argv[i+1]
            i += 2
        elif sys.argv[i] in ('-p', '--port', '--ports'):
            ports = [int(p) for p in sys.argv[i+1].split(',')]
            i += 2
        elif sys.argv[i] in ('-r', '--range'):
            ip_range = sys.argv[i+1]
            i += 2
        elif sys.argv[i] in ('-o', '--output'):
            out_file = sys.argv[i+1]
            i += 2
        elif sys.argv[i] in ('-q', '--quiet'):
            verbose = False
            i += 1
        else:
            print(f'Unknown arg: {sys.argv[i]}')
            sys.exit(1)

    if not (in_file and ip_range):
        print('Missing arg')
        sys.exit(1)

    with open(out_file, 'w+') as of:
        for proxy in get_ip(ip_range):
            for port in ports:
                if verbose:
                    print(f"port {port}")
                for user, password in get_creds(in_file):
                    if verbose:
                        print(f"{user}/{password}")
                    ret = helper.try_login(proxy, port, user, password, verbose)
                    if ret == cx_status.CONNECTED:
                        if verbose:
                            print(f"{user}:{password}@{proxy}:{port} OK")
                        of.write(f"{user}:{password}@{proxy}:{port}\n")
                        break
                    elif ret == cx_status.NOT_LISTENING:
                        if verbose:
                            print(f"Nothing is listening on port {port}")
                        break
                    else:
                        if verbose:
                            print(f"{user}:{password}@{proxy}:{port} ko")
                if ret == cx_status.NOT_LISTENING:
                    continue


if __name__ == '__main__':
    main(sys.argv)
