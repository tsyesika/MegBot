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

"""This is called when the bot recives a QUIT.
Once that has happened we assume we want to reconnect so it'll set
the bots 'running' attribute to false, this will trigger the connection
loop to re-initate the connection.
"""

def main(connection, command):
    """
    This will tell the bot to reconnect by setting a variable
    inside the bot to be False, this will cause it to run through the reconnection.:
    """
    if command.nick == connection.settings["nick"]:
        # Bot quit.
        # initate reconnect.
        connection.running = False
