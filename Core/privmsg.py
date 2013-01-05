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

"""This will send a privmsg to the IRCd.
This will send a privmsg to the IRCd, it'll handle messages
that are too long and would be truncated by the IRC by splitting them
up and sending them as seporate messages.

A valid call to this would be

    main(<connection>, "#channel", "message to send")

Todo: Stop this splitting up words and possibly place an elipsis (...) 
        on the end of messages to indecate the next one is meant to go 
        together (maybe prefix the next one also with ...).
"""

def main(connection, channel, message):
    """ Sends a PRIVMSG """
    # Todo, stop it chopping words up.
    
    pre_message = "PRIVMSG %s :" % (channel)

    # Max length of message can be 510 
    # (512 inc. \r\n so 510 as raw adds those).
    # See section 2.3 of RFC1459
    
    max_length = 510 - len(pre_message)
    messages = []
    for i in range(0, len(message), max_length):
        messages.append(message[i:i+max_length])
    
    # now send to raw.
    for message in messages:
        connection.core["Coreraw"].main(connection, "%s%s" % 
                                                             (pre_message, 
                                                                 message))
