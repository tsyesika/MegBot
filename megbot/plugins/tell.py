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

EVENT_ID = "tellEvent"
DATABASE_STR = "Tell.{}"


def main(connection, info):
    """
    Looks for the last time the user spoke and reports it.
    """
    store = connection.libraries["store"]
    if len(info.args) < 2:
        info.channel.send(u"Please specify a user and a message")
        return

    nick = info.args[0]
    msg = {"teller": info.nick, "msg": u" ".join(info.args[1:])}

    if nick == connection.settings["nick"]:
        info.channel.send(u"I can't tell myself anything, I'm all 1s and 0s")
        return

    db_name = DATABASE_STR.format(connection.name)
    try:
        tell = store.Store(db_name)
    except IOError:
        tell = store.Store(db_name, {})

    if info.channel_name in tell:
        if nick in tell[info.channel_name]:
            tell[info.channel_name][nick].append(msg)
        else:
            tell[info.channel_name][nick] = [msg]
    else:
        tell[info.channel_name] = {nick: [msg]}

    tell.save()
    info.channel.send(u"Got it.")


def on_PRIVMSG(connection, info):
    store = connection.libraries["store"]
    try:
        tell = store.Store(DATABASE_STR.format(connection.name))
    except IOError:
        # there are no messages
        return

    if info.channel_name in tell and info.nick in tell[info.channel_name]:
        for msg in tell[info.channel_name][info.nick]:
            info.channel.send(u'%s, %s says "%s"' % (info.nick, msg["teller"], msg["msg"]))

        del tell[info.channel_name][info.nick]
        tell.save()


def init(connection):
    info = connection.libraries["IRCObjects"].Info()

    # if a user is in the tell database speaks, send them any stored messages.
    info.action = "PRIVMSG"
    event = connection.core["Corehandler"].IRCEvent(info, on_PRIVMSG, EVENT_ID)
    connection.handler.register_event(event)


def unload(connection):
    connection.handler.unregister_event(EVENT_ID)


help = u"Send someone a message next time they speak in channel"
