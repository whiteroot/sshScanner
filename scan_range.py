#!/usr/bin/env python3

import sys
from ipaddress import ip_network

import helper
from constants import cx_status

timeout = 10
verbose = True
in_file = None
u_file = None
p_file = None


def get_ip(cidr):
    net = ip_network(cidr, strict=False)
    for ip in net:
        yield str(ip)


def treat_ip(ip, ports, of):
    if verbose:
        print(f"IP: {ip}")
    for port in ports:
        treat_port(ip, port, of)


def treat_port(ip, port, of):
    open_ports = []
    if verbose:
        print(f"port {port}")
    if in_file:
        with open(in_file, 'r') as f:
            for line in f:
                x = line.split('|')
                user, password = x[0], x[1].strip()
                status = connect_user_password(ip, port, user, password, of)
                if status in (cx_status.CONNECTED, cx_status.NOT_LISTENING):
                    return status
                else:
                    ip_port = f"{ip}:{port}"
                    if ip_port not in open_ports:
                        open_ports.append(ip_port)
                        with open(f"{out_file}.open", "a") as opf:
                            opf.write(f"{ip_port}\n")
    else:
        with open(u_file, 'r') as uf:
            with open(p_file, 'r') as pf:
                for user in uf:
                    for password in pf:
                        status = connect_user_password(ip, port, user.strip(), password.strip(), of)
                        if status in (cx_status.CONNECTED, cx_status.NOT_LISTENING):
                            return status
                        else:
                            ip_port = f"{ip}:{port}"
                            if ip_port not in open_ports:
                                open_ports.append(ip_port)
                                with open(f"{out_file}.open", "a") as opf:
                                    opf.write(f"{ip_port}\n")


def connect_user_password(ip, port, user, password, of):
    ret = helper.try_login(ip, port, user, password, verbose, timeout)
    if ret == cx_status.CONNECTED:
        if verbose:
            print(f"{user}:{password}@{ip}:{port} OK")
        of.write(f"{user}:{password}@{ip}:{port}\n")
    elif ret == cx_status.NOT_LISTENING:
        if verbose:
            print(f"Nothing is listening on port {port}")
    else:
        if verbose:
            print(f"{user}:{password}@{ip}:{port} ko")
    return ret


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
    for ip in get_ip(ip_range):
        treat_ip(ip, ports, of)
