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

"""This is called when you enter a channel, it will parse the line
which lists the peopel in the channel and produce a dictionary with
the value of a list. The list will contain all the members of that
paticular type (e.g. half op (hop), vop (voiced), etc...

The list isn't returned by main but added directly to <connection>.channels
(i.e. the channel attribute on the bot instance which calls it. This is done
via the connection you pass to it (as it's first argument).
"""

def main(connection, message):
    """Names on joining of a channel"""
    channel = message.split("#")[1].split()[0]
    nicks = message.split(":")[2].split()
    connection.channels[channel] = {"all":[], "hop":[], "sop":[], "aop":[], "vop":[], "non":[], "founder":[]}
    for nick in nicks:
        if nick[0] in ["+", "&", "@", "%", "~"]:
            connection.channels[channel][bot.config.permissions[nick[0]]].append(nick[1:])
            connection.channels[channel]["all"].append(nick[1:])
        else:
            connection.channels[channel]["non"].append(nick)
            connection.channels[channel]["all"].append(nick)
