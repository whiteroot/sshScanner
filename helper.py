import getpass
import sys

from constants import cx_status

import paramiko


# setup logging
paramiko.util.log_to_file("/tmp/paramiko.log")
# Paramiko client configuration
UseGSSAPI = ( paramiko.GSS_AUTH_AVAILABLE)
DoGSSAPIKeyExchange = ( paramiko.GSS_AUTH_AVAILABLE)


def try_login(hostname, port, username, password, verbose, timeout):
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        if verbose:
            print("Trying to connect... {}/{}@{}:{}".format(username, password, hostname, port))
        if not UseGSSAPI and not DoGSSAPIKeyExchange:
            try:
                client.connect(hostname, port, username, password,
                        timeout=timeout, banner_timeout=timeout, auth_timeout=timeout)
            except paramiko.ssh_exception.NoValidConnectionsError:
                return cx_status.NOT_LISTENING
            except Exception:
                try:
                    client.close()
                except Exception:
                    pass
                return cx_status.ERROR
        else:
            raise ("not tested code")
            try:
                client.connect( hostname, port, username, gss_auth=UseGSSAPI, gss_kex=DoGSSAPIKeyExchange,
                        timeout=timeout, banner_timeout=timeout, auth_timeout=timeout)
            except Exception:
                password = getpass.getpass( "Password for %s@%s: " % (username, hostname))
                try:
                    client.connect(hostname, port, username, password,
                            timeout=timeout, banner_timeout=timeout, auth_timeout=timeout)
                    try:
                        client.close()
                    except Exception:
                        pass
                except Exception:
                    try:
                        client.close()
                    except Exception:
                        pass
                    return cx_status.ERROR

        chan = client.invoke_shell()
        chan.close()
        client.close()
        return cx_status.CONNECTED

    except Exception as e:
        print("*** Caught exception: %s: %s" % (e.__class__, e))
        try:
            client.close()
        except:
            pass
        return cx_status.ERROR
