##
#
# -*- coding: utf-8 -*-
#
#   This file is part of MegBot
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
#
##

import re


BEERTIME = re.compile(r"^[^!].*(beer\s*time)", re.IGNORECASE|re.UNICODE)

eventID = 'beerEvent'

def on_PRIVMSG(connection, info):
    channel = connection.channels[info.channel]
    if BEERTIME.search(info.message):
        channel.send(
            "When you're a {botname}, it's always beertime.".format(
            botname=connection.settings["nick"])
        )


def init(connection):
    info = connection.libraries["IRCObjects"].Info()

    # this will peform an event on privmsg.
    info.action = "PRIVMSG"
    event = connection.core["Corehandler"].IRCEvent(info, on_PRIVMSG, eventID)
    connection.handler.register_event(event)


def unload(connection):
    connection.handler.unregister_event(eventID)

help = u"Something to do with Potatoes"
