#!/usr/bin/env python3

import sys
from ipaddress import ip_network
import concurrent.futures
import threading

from scanner import Scanner
import helper
from constants import cx_status

timeout = 10
verbose = True
in_file = None
u_file = None
p_file = None

thread_local = threading.local()


def get_scanner(ip, ports, u_file, p_file, in_file, verbose, timeout, of):
    if not hasattr(thread_local, "scanner"):
        thread_local.scanner = Scanner(ip, ports, u_file, p_file, in_file, verbose, timeout, of)
    return thread_local.scanner


def get_ip(cidr):
    net = ip_network(cidr, strict=False)
    for ip in net:
        yield str(ip)


def scan_ip(ip):
    scanner = get_scanner(ip, ports, u_file, p_file, in_file, verbose, timeout, of)
    scanner.scan_ip()


out_file = '/tmp/ssh_scan_results.txt'
ip_range = None
ports = [22]  # default port list
argc = len(sys.argv)
i = 1
while (i < argc):
    if sys.argv[i] in ('-i', '--input'):
        in_file = sys.argv[i+1]
        i += 2
    elif sys.argv[i] in ('-fu', '--users'):
        u_file = sys.argv[i+1]
        i += 2
    elif sys.argv[i] in ('-fp', '--passwords'):
        p_file = sys.argv[i+1]
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
    elif sys.argv[i] in ('-t', '--timeout'):
        timeout = int(sys.argv[i+1])
        i += 2
    else:
        print(f'Unknown arg: {sys.argv[i]}')
        sys.exit(1)

if not ip_range:
    print('Missing arg')
    sys.exit(1)
if not (in_file or (u_file and p_file)):
    print('Missing arg')
    sys.exit(1)

with open(f"{out_file}.cracked", 'a') as of:
    with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:
        executor.map(scan_ip, get_ip(ip_range))
