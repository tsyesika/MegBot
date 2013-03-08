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

"""CTCP
"""

eventID = "PingEvent"

def request(connection, target, message, command):
    """Send a CTCP request to target"""

    message = "\x01%s %s\x01" % (command, message)
    connection.core["Coreprivmsg"].main(connection, target, message)

def reply(connection, target, message, command):
    """Send a CTCP reply to target"""

    message = "\x01%s %s\x01" % (command, message)
    connection.core["Corenotice"].main(connection, target, message)

def on_CTCP(connection, info):
    def on_PING():
        connection.core["Corectcp"].reply(connection, info.nick, data, "PING")

    def on_VERSION():
        version = connection.config.ctcp_options["version"]
        connection.core["Corectcp"].reply(connection, info.nick, version, "VERSION")
        

    command = {
                "PING":     on_PING,
                "VERSION":  on_VERSION
                }

    data = " ".join(info.args)
    data = data[:data.find("\x01")]

    command[info.plugin_name]()
        

def load(connection):
    eventInfo = connection.libraries["IRCObjects"].Info()
    eventInfo.action = "PRIVMSG"
    eventInfo.trigger = "\x01"
    
    event = connection.handler.IRCEvent(eventInfo, on_CTCP, eventID)
    connectiion.handler.register_event(event)
