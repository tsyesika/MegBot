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

"""This is called when a mode is changed in a channel.
It will update the bot's channels attribute, the channels
attribute holds information about a specific channel (including
the user list split into different types (sop, aop, hop, etc...)

When a MODE command is issued it will check if it's a mode which
changes the mode of a user in a channel (giving them ops, founder, etc...)
if it is, the instances list will be updated accordingly, this ensures
calls to any library which depends on these will get the correct information
and not stale information from when the bot joined the channel.
"""


def main(connection, line):
    """When a mode is set"""
    mode = line[3][1:]
    channel = line[2] # we store them with the hash(s) :)
    if "#" != channel[0]:
        # not a channel, we not fussed.
        return
    for v1, m in enumerate(mode):
        if m in ["a", "o", "q", "h", "v"]:
            if len(line) <= 3:
                nick = line[0][1:].split("!")[0]
            else:
                nick = line[4:][v1]
            if m == "a":
                connection.channels[channel]["sop"].append(nick)
            elif m == "o":
                connection.channels[channel]["aop"].append(nick)
            elif m == "h":
                connection.channels[channel]["hop"].append(nick)
            elif m == "v":
                connection.channels[channel]["vop"].append(nick)
            elif m == "q":
                connection.channels[channel]["founder"].append(nick)
