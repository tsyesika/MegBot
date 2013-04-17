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

"""This is to send raw messages.
This will automatically append \r\n unless specified.
The plugin should be used to send unaltered messages directly
to the IRCd. If you wish to send a PRIVMSG, JOIN, PART, etc...
please consider using the core plugins available to do that.

This plugin also will display the message on stdout (via print).
the message will displayed with [OUT] in square breakets. The
sendall is used instead of send in this plugin to avoid it simply
being appended to the buffer. The 'sendall' method will send it even
if the buffer isn't full (ensuring the message is delivered as soon as
the function is called).

NB: The IRCd must have the ending \r\n as defined in the IRC RFCs for
    it to be a valid message. you should be able to break messages up
    over several lines providing the last line has \r\n.

    If you don't have that when you send another message to the IRCd it'll
    assume it's part of this message and cause an invalid message to be sent.
"""

def main(connection, message, sock=None, end="\r\n"):
    """ Sends a PRIVMSG """
    if not sock:
        sock = connection.sock
    print "[OUT] %s" % message
    sock.sendall(("%s%s" % (message, end)).encode("utf-8"))
    return
