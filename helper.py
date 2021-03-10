import getpass
import sys

import paramiko


# setup logging
paramiko.util.log_to_file("/tmp/paramiko.log")
# Paramiko client configuration
UseGSSAPI = ( paramiko.GSS_AUTH_AVAILABLE)
DoGSSAPIKeyExchange = ( paramiko.GSS_AUTH_AVAILABLE)


def try_login(hostname, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        print("Trying to connect... {}/{}@{}:{}".format(username, password, hostname, port))
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
        print("Match!!!")
        chan.close()
        client.close()
        return True

    except Exception as e:
        print("*** Caught exception: %s: %s" % (e.__class__, e))
        try:
            client.close()
        except:
            pass
        return False
