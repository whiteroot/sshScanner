#!/usr/bin/env python3

import sys

import helper


def get_proxies(f):
    with open(f, 'r') as f:
        for line in f:
            x = line.split('|')
            yield x[0], x[1], x[2].strip()

def main(argv):
    _file = None
    ports = [22]  # default port list
    argc = len(sys.argv)
    i = 1
    while (i < argc):
        if sys.argv[i] in ('-f', '--file'):
            _file = sys.argv[i+1]
            proxies = get_proxies(_file)
            i += 2
        elif sys.argv[i] in ('-p', '--port', '--ports'):
            ports = [int(p) for p in sys.argv[i+1].split(',')]
            i += 2

    if not _file:
        print('Missing file arg')
        sys.exit(1)

    for proxy, user, password in proxies:
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
