#!/usr/bin/env python2

import getpass
import sys
import traceback

import paramiko


# setup logging
paramiko.util.log_to_file("/tmp/paramiko.log")
# Paramiko client configuration
UseGSSAPI = ( paramiko.GSS_AUTH_AVAILABLE)
DoGSSAPIKeyExchange = ( paramiko.GSS_AUTH_AVAILABLE)


def get_proxies(f):
    with open(f, 'r') as f:
        for line in f:
            x = line.split('|')
            yield x[0], x[1], x[2]

def try_login(hostname, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        print "Trying to connect... {}/{}@{}:{}".format(username, password, hostname, port)
        if not UseGSSAPI and not DoGSSAPIKeyExchange:
            try:
                client.connect(hostname, port, username, password)
            except Exception:
                try:
                    client.close()
                except Exception:
                    pass
                return False
        else:
            raise ("not tested code")
            try:
                client.connect( hostname, port, username, gss_auth=UseGSSAPI, gss_kex=DoGSSAPIKeyExchange)
            except Exception:
                # traceback.print_exc()
                password = getpass.getpass( "Password for %s@%s: " % (username, hostname))
                try:
                    client.connect(hostname, port, username, password)
                    try:
                        client.close()
                    except Exception:
                        pass
                except Exception:
                    try:
                        client.close()
                    except Exception:
                        pass
                    return False

        chan = client.invoke_shell()
        print(repr(client.get_transport()))
        print "Match!!!"
        chan.close()
        client.close()
        return True

    except Exception as e:
        print("*** Caught exception: %s: %s" % (e.__class__, e))
        traceback.print_exc()
        try:
            client.close()
        except:
            pass
        return False

def main(argv):
    _file = None
    ports = [22]
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

    for proxy, user, password in proxies:
        for port in ports:
            try:
                ret = try_login(proxy, port, user, password)
                if ret:
                    print "{}:{}@{}:{} OK".format(user, password, proxy, port)
                    break
                else:
                    print "{}:{}@{}:{} ko".format(user, password, proxy, port)
            except Exception as e:
                print "{}:{}@{}:{} ko".format(user, password, proxy, port)


if __name__ == '__main__':
    main(sys.argv)
