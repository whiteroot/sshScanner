import sys
from ipaddress import ip_network
from time import sleep
from random import random

import helper
from constants import cx_status

_9hits_sep = '|'
NB_ATTEMPTS = 3


class Scanner(object):

    def __init__(self, ip, ports, u_file, p_file, in_file, verbose, timeout, of):
        self.ip = ip
        self.ports = ports
        self.u_file = u_file
        self.p_file = p_file
        self.in_file = in_file
        self.verbose = verbose
        self.timeout = timeout
        self.of = of
        self.open_ports = []


    def store_open_ip_port(self):
        return
        ip_port = f"{self.ip}:{self.port}"
        if ip_port not in self.open_ports:
            self.open_ports.append(ip_port)
            with open(f"{out_file}.open", "a") as opf:
                opf.write(f"{ip_port}\n")


    def scan_ip(self):
        if self.verbose:
            print(f"IP: {self.ip}")
        for self.port in self.ports:
            self.treat_port()


    def treat_port(self):
        if self.verbose:
            print(f"port {self.port}")
        if self.in_file:
            with open(in_file, 'r') as f:
                for line in f:
                    x = line.split('|')
                    user, password = x[0], x[1].strip()
                    status = self.connect_user_password(user, password)
                    if status in (cx_status.CONNECTED, cx_status.NOT_LISTENING):
                        return status
                    else:
                        self.store_open_ip_port()
        else:
            with open(self.u_file, 'r') as uf:
                with open(self.p_file, 'r') as pf:
                    for user in uf:
                        for password in pf:
                            status = self.connect_user_password(user.strip(), password.strip())
                            if status in (cx_status.CONNECTED, cx_status.NOT_LISTENING):
                                return status
                            else:
                                self.store_open_ip_port()


    def connect_user_password(self, user, password):
        ret = self.try_login(user, password)
        if ret == cx_status.CONNECTED:
            if self.verbose:
                print(f"{user}:{password}@{self.ip}:{self.port} OK")
            self.of.write(f"{self.ip}:{self.port}{_9hits_sep}{user}{_9hits_sep}{password}\n")
        elif ret == cx_status.NOT_LISTENING:
            if self.verbose:
                print(f"Nothing is listening on port {self.port}")
        else:
            if self.verbose:
                print(f"{user}:{password}@{self.ip}:{self.port} ko")
        return ret

    def try_login(self, user, password):
        for i in range(NB_ATTEMPTS):
            sleep(random())
            t = i * 2
            print(f'retry after {t} sec...')
            sleep(t)
            if self.verbose:
                print(f"attempt at {self.ip}:{self.port} = {i+1}")
            ret = helper.try_login(self.ip, self.port, user, password, self.verbose, self.timeout)
            if ret in (cx_status.CONNECTED, cx_status.ERROR):
                print('port is open!')
                return ret
        return ret
