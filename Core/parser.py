#This file is part of MegBot.
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

"""This is called when the bot wants data from the IRCd
It'll call recv on the socket (which will return "" when the
connection has been dropped (by the remote end). This will 
switch the 'running' variable on the bot which will initrate
the reconnection. 

If the message is filled it will fill a list with less than or
equal to 2048 bytes of data. This is then checked to see if it's
the end of a message (IRC messages will be ended by \r\n. If it has
it'll return the message back to the bot for parsing, validaiton and
then execution.

If it isn't ended with \r\n it suggests that the IRCd hasn't finished
giving it some messages and ask for more before sending it back to the
bot.

It can be the case that there are multiple messages returned by this. To
break them into indevidual messages you should split the returned string by
"\r\n" e.g:

    returned_string.split("\r\n")

that will produce a list of each indevidual message.

Todo: handle in the unlikely situation the socket at our end is closed which
        should produce a socket.error exception, this can then be handled with
        the remote socket close (i.e. initiate a reconnect).
"""

def main(connection, message=[]):
    """ Parses the text """
    message.append(connection.sock.recv(2048))
    if message[-1] == "":
        # Socket broken
        connection.running = False
        return ""
    if message[-1][-2:] == "\r\n":
        return "".join(message)
    return main(connection, message)
