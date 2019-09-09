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

from datetime import datetime, timedelta
from threading import RLock
import logging
import random
import re

_log = logging

EVENT_ID = "replyMsg"
DATABASE_STR = "replies.{}"
CHATTINESS = 30  # where 100 would be reply all the time
SHUTUP_SECONDS = 30 * 60  # how long to shutup for

_cache = []
_what_you_said = {}
_lock = RLock()

_shutup = {}
_shutup_lock = RLock()


class Reply(object):
    valid_options = ["reply", "chance", "flags"]

    def __init__(self, msg, channel):

        self.channel = channel
        self.regex, self.regex_compiled, self.options = self.parse_msg(msg)

    def parse_msg(self, msg):
        # msg = "cloud<reply>butt<chance>999"
        msg_split = msg.split("<")

        regex = msg_split[0]
        options = {}
        for opt in msg_split[1:]:
            key, value = opt.split(">")
            if key not in self.valid_options:
                raise Exception(u"{} is not a valid option".format(key))
            options[key] = value

        if "reply" not in options:
            raise Exception("Specify a reply")

        flags = re.UNICODE
        if "i" in options.get("flags", ""):
            flags = flags | re.IGNORECASE
        regex_compiled = re.compile(regex, flags=flags)

        return regex, regex_compiled, options

    def serialize(self):
        output = [self.regex]
        for k, v in self.options.items():
            output.append(u"<{}>{}".format(k, v))

        return u"".join(output), self.channel

    def sub(self, info):
        if info.channel_name != self.channel:
            return

        chance = self.options.get("chance", None)

        if chance is None:
            chance = CHATTINESS * 0.01
        else:
            chance = int(chance) * CHATTINESS * 0.0001

        rand = random.random()
        if rand < chance:
            if self.regex_compiled.search(info.message):
                return self.options["reply"]


def open_database(connection):
    store = connection.libraries["store"]
    db_name = DATABASE_STR.format(connection.name)
    try:
        replies = store.Store(db_name)
        replies["rules"]
    except (IOError, KeyError):
        replies = store.Store(db_name, {"rules": []})
        with _lock:
            replies.save()

    return replies


def main(connection, info):
    try:
        msg = u" ".join(info.args)
        reply_obj = Reply(msg, info.channel_name)
    except Exception:
        _log.exception("Could not parse reply")
        info.channel.send(u"I understand... not")
        return

    with _lock:
        idx = len(_cache)
        replies = open_database(connection)
        replies["rules"].append(reply_obj.serialize())
        err = False
        try:
            replies.save()
        except Exception:
            # don't send data while in a lock, set this and send out error
            # message later
            err = True
            _log.exception("Couldn't save replies database")
        else:
            _cache.append(reply_obj)

    if err:
        info.channel.send(u"I understand... but I can't save that to my database")
    else:
        info.channel.send(u"I understand ({})".format(idx))


def on_PRIVMSG(connection, info):
    key = "{}#{}".format(connection.name, info.channel_name)
    with _shutup_lock:
        if key in _shutup:
            if datetime.utcnow() > _shutup[key]:
                del _shutup[key]
            else:
                return

    for reply in _cache:
        msg = reply.sub(info)
        if msg is not None:
            info.channel.send(msg)
            key = "{}#{}".format(connection.name, info.channel_name)
            _what_you_said[key] = reply
            return


def on_what_now(connection, info):
    key = "{}#{}".format(connection.name, info.channel_name)
    try:
        with _lock:
            reply = _what_you_said[key]
            try:
                idx = u"({}) ".format(_cache.index(reply))
            except ValueError:
                idx = u""
            msg = u"{}: reply was based on {}{}".format(info.nick, idx, reply.serialize()[0])
    except KeyError:
        info.channel.send(u"I didn't say anything")
    else:
        info.channel.send(msg)


def on_remove_reply(connection, info):
    error = False
    try:
        if len(info.args) != 1:
            raise TypeError

        idx = int(info.args[0])
    except (TypeError, IndexError, ValueError):
        info.channel.send(u"Cannot remove that")
        return

    with _lock:
        replies = open_database(connection)
        try:
            _cache[idx]
        except IndexError:
            error = True
        else:
            del _cache[idx]
            del replies["rules"][idx]
            try:
                replies.save()
            except Exception:
                _log.exception("Couldn't save replies database")
    if error:
        info.channel.send(u"Something went wrong.")
    else:
        info.channel.send(u"{} deleted".format(idx))


def on_shutup(connection, info):
    key = "{}#{}".format(connection.name, info.channel_name)
    with _shutup_lock:
        if key in _shutup:
            _shutup[key] += timedelta(seconds=SHUTUP_SECONDS)
        else:
            _shutup[key] = datetime.utcnow() + timedelta(seconds=SHUTUP_SECONDS)
    info.channel.send("Shutting up until {}".format(_shutup[key].strftime("%Y-%m-%d %H:%M:%S")))


def init(connection):
    with _lock:
        replies = open_database(connection)

        for reply in replies["rules"]:
            reply_obj = Reply(*reply)
            _cache.append(reply_obj)

    # listens for matching messages
    listen = connection.libraries["IRCObjects"].Info()
    listen.action = "PRIVMSG"
    event = connection.core["Corehandler"].IRCEvent(listen, on_PRIVMSG, EVENT_ID)
    connection.handler.register_event(event)

    # !what was that?
    what = connection.libraries["IRCObjects"].Info()
    what.action = "PRIVMSG"
    what.plugin_name = "what"
    what.args = ["was", "that?"]
    what.trigger = connection.settings["trigger"]
    event = connection.core["Corehandler"].IRCEvent(what, on_what_now, EVENT_ID)
    connection.handler.register_event(event)

    # !removeReply <int>
    remove = connection.libraries["IRCObjects"].Info()
    remove.action = "PRIVMSG"
    remove.plugin_name = "remove"
    remove.trigger = connection.settings["trigger"]
    event = connection.core["Corehandler"].IRCEvent(remove, on_remove_reply, EVENT_ID)
    connection.handler.register_event(event)

    # !shutup
    shutup = connection.libraries["IRCObjects"].Info()
    shutup.action = "PRIVMSG"
    shutup.plugin_name = "shutup"
    shutup.trigger = connection.settings["trigger"]
    event = connection.core["Corehandler"].IRCEvent(shutup, on_shutup, EVENT_ID)
    connection.handler.register_event(event)


def unload(connection):
    connection.handler.unregister_event(EVENT_ID)


help = u"regex<reply>reply<chance>100"
