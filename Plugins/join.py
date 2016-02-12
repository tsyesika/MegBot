##
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

def main(connection, info):
    if not info.args:
        # Being called by bot.
        return
    if "Channel" in dir():
        Channel.send(u"Please specify a channel to join.")
        return
    Server.join(Info.args[0])
    Channel.send(u"%s joined.", Info.args[0])

help = u"Tries to join the specified channel."
