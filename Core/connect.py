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


import socket
from time import sleep

def main(connection):
    """ Connects to irc (by setting up socket and passing info to ircd) """

    if connection.settings["ssl"]:
        # The import here is because some systems don't ship it,
        # we only care about them not doing if they're using ssl
        # If they do want ssl and it's not here, a exception should
        # be raised and handled further up the code base.

        import ssl
        connection.sock = ssl.wrap_socket(connection.sock)
  
    connected = False

    while not connected:
        try:
            connection.sock.connect((connection.settings["address"], 
                                     connection.settings["port"]))
            connected = True

        except socket.error:
            # We want to wait here. Hitting the server too much
            # isn't a good idea, if they haven't specified a 
            # network specific timeout or a global one we'll use
            # 10 seconds as it's a sensible time. 

            timeout = 10 # default, 10 seconds.
            
            if "timeout" in connection.settings.keys():
                timeout = connection.settings["timeout"]
            elif "timeout" in dir(connection.config):
                timeout = connection.config.timeout
            
            sleep(timeout)
   
    connection.core["Coreraw"].main(connection, 
                                    "NICK %s" % (
                                                connection.settings["nick"]
                                                )
                                    )
    connection.core["Coreraw"].main(connection, 
                                    "USER 8 * %s :%s" % 
                                        (
                                        connection.settings["ident"], 
                                        connection.settings["realname"]
                                        )
                                   )
    connection.running = True
