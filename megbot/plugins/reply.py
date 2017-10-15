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

import random
import re


EVENT_ID = "replyMsg"
DATABASE_STR = "replies.{}"
CHATTINESS = 30  # where 100 would be reply all the time

_cache = {}

_what_you_said = {}

class Reply(object):
    valid_options = ["reply", "chance"]

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

        regex_compiled = re.compile(regex)

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


def main(connection, info):
    store = connection.libraries["store"]

    try:
        msg = u" ".join(info.args)
        reply_obj = Reply(msg, info.channel_name)
    except Exception:
        info.channel.send(u"I understand... not")
        return

    db_name = DATABASE_STR.format(connection.name)
    replies = store.Store(db_name)
    replies[reply_obj.regex] = reply_obj.serialize()
    replies.save()
    _cache[reply_obj.regex] = reply_obj
    info.channel.send(u"I understand")


def on_PRIVMSG(connection, info):
    for reply in _cache.values():
        msg = reply.sub(info)
        if msg is not None:
            info.channel.send(msg)
            key = "{}#{}".format(connection.name, info.channel_name)
            _what_you_said[key] = reply


def on_what_now(connection, info):
    key = "{}#{}".format(connection.name, info.channel_name)
    if key in _what_you_said:
        msg = u"{}: reply was based on {}".format(info.nick, _what_you_said[key].serialize()[0])
        info.channel.send(msg)
    else:
        info.channel.send(u"I didn't say anything")


def init(connection):
    store = connection.libraries["store"]
    db_name = DATABASE_STR.format(connection.name)
    try:
        replies = store.Store(db_name)
    except IOError:
        replies = store.Store(db_name, {})
        replies.save()

    for reply in replies.values():
        reply_obj = Reply(*reply)
        _cache[reply_obj.regex] = reply_obj

    info = connection.libraries["IRCObjects"].Info()

    # this will peform an event on privmsg.
    info.action = "PRIVMSG"
    event = connection.core["Corehandler"].IRCEvent(info, on_PRIVMSG, EVENT_ID)
    connection.handler.register_event(event)

    info = connection.libraries["IRCObjects"].Info()
    info.action = "PRIVMSG"
    info.plugin_name = "what"
    info.args = ["was", "that?"]
    event = connection.core["Corehandler"].IRCEvent(info, on_what_now, EVENT_ID)
    connection.handler.register_event(event)


def unload(connection):
    connection.handler.unregister_event(EVENT_ID)


help = u"regex<reply>reply<chance>100"
