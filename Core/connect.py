##
#   This file is part of MegBot.
#
#   MegBot is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   MegBot is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with MegBot.  If not, see <http://www.gnu.org/licenses/>.
##

""" This core module will connect to the IRCd specified in MegBot
It'll handle reconnection. Note this won't return back until the connection
has been made.

Todo: Support varify certs.
Todo: Have a reconnection limit support?
        (i.e. after 10 tries it'll give up.)
"""

import os
import socket
import sys
import traceback
from time import sleep

def setupConnection(connection, address, port, ipv6=True):
    """ Sets up socket and then connects """
    if ipv6:
        connection.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    else:
        # these are actually the default but it's more clear if we specify.
        connection.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connection.sock.connect((address, port))

def SSLWrapper(sock, verify):
    """ Wraps a socket in ssl - requires pythons ssl module """
    try:
        import ssl
        if not verify:
            # not verifying, just wrap and return
            return ssl.wrap_socket(sock)

        # okay now verifying.
        if not os.path.isfile("Data/cert.pem"):
            print "[ErrorLine] Data/cert.pem file doesn't exit, can't verify"
            sys.exit()

        return ssl.wrap_socket(sock, ca_certs="Data/cert.pem", cert_reqs=ssl.CERT_REQUIRED)

    except ImportError:
        print "[ErrorLine] No 'ssl' module, please install it."
    except:
        print "[ErrorLine] SSL error:"
        traceback.print_exc()
    # only if it's failed (as successful call would have return by now)
    try:
        sock.close()
    except:
        pass
    
    sys.exit()

def SendInfo(connection, nick, ident, realname, host=None):
    """ Sends the info such as NICK and USER to ircd """
    if not host:
        host = socket.gethostname()
        # be a good little bot and save it back
        connection.settings["hostname"] = host
    connection.core["Coreraw"].main(connection, "NICK %s" % (nick))
    connection.core["Coreraw"].main(connection, "USER %s %s %s: %s"
            %   (
                nick, ident, host, realname
                )
        )

def ReadConfig(connection):
    """ Reads all the config needed to connect """
    timeout = 10 # default, 10 seconds.
    hostname = None
    critError = []
    if "hostname" in connection.settings.keys():
        hostname = connection.settings["hostname"]

    if "timeout" in connection.settings.keys():
        timeout = connection.settings["timeout"]
    elif "timeout" in dir(connection.config):
        timeout = connection.config.timeout

    if "address" in connection.settings:
        address = connection.settings["address"]
    else:
        print "You need to specify an address to connect to."
        sys.exit()

    if "ipv6" in connection.settings:
        ipv6 = connection.settings["ipv6"]
    else:
        ipv6 = None # this will cause it to prefer ipv6 but fail to ipv4
    
    ssl_verify = False

    if "ssl" in connection.settings:
        ssl = connection.settings["ssl"]
        
        # Okay do they care about varification
        if "ssl_verify" in connection.settings:
            ssl_verify = connection.settings["ssl_verify"]

    else:
        ssl = None # laaa people likes ze insecure

    if "port" in connection.settings:
        try:
            port = connection.settings["port"]
        except ValueError:
            cirtError.append("Invalid port number: %s" % connection.settings["port"])
    else:
        cirtError.append("You need to specify a port.")
    
    if "nick" in connection.settings:
        nickname = connection.settings["nick"]
    else:
        critError.append("You need to specify an nickname.")

    if "ident" in connection.settings:
        ident = connection.settings["ident"]
    else:
        critError.append("You need to specify an ident.")

    if "realname" in connection.settings:
        realname = connection.settings["realname"]
    else:
        cirtError.append("You need to specify a realname.")

    if critError:
        print "[ErrorLine] The following errors with your config:"
        for error in critError:
            print "    %s" % error
        print "Because of above erros the bot %s won't start."
        print "Please fix the errors above."
        sys.exit()

    return {
        "address":address,
        "port":port,
        "nick":nickname,
        "ident":ident,
        "realname":realname,
        "timeout":timeout,
        "hostname":hostname,
        "ipv6":ipv6,
        "ssl":ssl,
        "ssl_verify":ssl_verify
    }


def main(connection):
    """ Connects to irc (by setting up socket and passing info to ircd) """

    connected = False
    IPCycle = [False, True] # done change the order
    config = ReadConfig(connection)
    ipv6 = config["ipv6"]
    attempts = 0

    while not connected:
        try:
            setupConnection(connection, config["address"], config["port"], ipv6)
            connected = True
        except socket.error:
            traceback.print_exc()
            if None == config["ipv6"]:
                # We haven't specified ipv6 so by default we've tried ipv6.
                # that could have caused this, lets try ipv4
                ipv6 = IPCycle[0]
                IPCycle.append(IPCycle.pop(0))
                if not attempts:
                    # we ought not to wait around.
                    continue
            # lets not hammer the server
            sleep(config["timeout"])

    if config["ssl"]:
        connection.sock = SSLWrapper(connection.sock, config["ssl_verify"])

    SendInfo(connection, config["nick"], config["port"], config["realname"], config["hostname"])

    connection.running = True


