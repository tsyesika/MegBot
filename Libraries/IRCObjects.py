# -*- coding: utf-8 -*-
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
#   also along with MegBot.  If not, see <http://www.gnu.org/licenses/>.
##

import time
import re
import platform
import os
import urllib2
import urllib
import HTMLParser
from datetime import datetime

from types import *


class Standard(object):
    """ Never instantiate """
    def __setuphooks__(self, connection):
        """ Sets up hooks for the class
        Any method on the class (inhereted) that begins with
        the prefix on_ will be automatically registered with
        the hooker
        """
        if "Corehooker" in connection.core:
            # Woot, we got ability to have hooks
            for method in dir(self):
                if method.startswith("on_"):
                    connection.hooker.register_hook(method, eval("self.%s" % method))

class Info(Standard):
    def __init__(self, line=None, connection=None):
        self.connection = connection

        if line == None:
            # Make an empty Info.
            self.nick = u""
            self.ident = u""
            self.hostname = u""
            self.nickmask = tuple()
            self.parsed = tuple()
            self.action = u""
            self.raw = u""
            self.message = u""
            self.channel_name = u""
            self.plugin_name = u""
            self.trigger = u""
            self.args = []
            return

        # Lets pull things out.
        self.raw = line
        self.parsed = self.parseIRC(line)
        
        if self.parsed and len(self.parsed) == 6:
            self.nickmask, self.action, self.channel_name, self.trigger, self.plugin_name, self.args = self.parsed
        elif self.parsed:
            self.nickmask, self.action, self.args = self.parsed
            self.channel_name, self.trigger, self.plugin_name = (u"", u"", u"")
        else:
            return self.__init__(None)

        # Gets elements from nickmask
        if self.nickmask:
            self.nick, self.ident, self.hostname = self.nickmask
        else:
            self.nick, self.ident, self.hostname = (u"", u"", u"")

        self.message = "%s%s %s" % (self.trigger, self.plugin_name, " ".join(self.args))

    def parseHostMask(self, nickmask):
        """ Parses the nickmask """
        if len(nickmask) <= 1:
            # can happen =[
            return (u"", u"", u"")

        if "@" in nickmask:
            nickmask, host = nickmask.split("@", 1)
        else:
            host = u""

        if "!" in nickmask:
            nickname, ident = nickmask.split("!", 1)
            if ":" == nickname[0]:
                # why is this happening?
                nickname = nickname[1:]
        else:
            nickname, ident = (u"", u"")

        return nickname, ident, host

    def parseIRC(self, message):
        """ Parses out IRC message (in accordance with RFC """
        if not message:
            # empty message, sod off.
            return ()

        if ":" == message[0]:
            # We can expect a hostmak now.
            hostmask, message = message.split(" ", 1)
            hostmask = self.parseHostMask(hostmask)
        else:
            hostmask = ""

        if ":" in message and ":" != message[-1]:
            args = message.split(":", 1)[1]
            trigger = args[0]
            args = args.split(" ")
            plugin_name = args[0][1:]

        else:
            args = []
            trigger = ""
            plugin_name = ""

        message = message.split()

        if len(message) >= 3:
            return (hostmask, message[0], message[1], trigger, plugin_name, args[1:])
        else:
            return (hostmask, message[0], args)

    @property
    def channel(self):
        if self.connection is None:
            return None
        else:
            return self.connection.channels[self.channel_name]

class L_Helper(Standard):
    def __init__(self):
        self.HTMLTagRe = re.compile(r'<[^<]+?>')
        self.HTMLParser = HTMLParser.HTMLParser()

        self.time_units = (
            (60 * 60 * 24 * 365 * 1000000, "%d millennium", "%d millennia"), # millennia
            (60 * 60 * 24 * 365 * 100, "%d century", "%d centuries"), # centuries
            (60 * 60 * 24 * 365 * 10, "%d decade", "%d decades"), # decades
            (60 * 60 * 24 * 365, "%d year", "%d years"), # years
            (60 * 60 * 24 * 30, "%d month", "%d months"), # months
            (60 * 60 * 24 * 7, "%d week", "%d weeks"), # weeks
            (60 * 60 * 24, "%d day", "%d days"), # days
            (60 * 60, "%d hour", "%d hours"), # hour
            (60, "%d minute", "%d minutes"), # minute      
        )

    def StripHTML(self, message):
        """ This strips the HTML off a specific message """
        return self.HTMLTagRe.sub("", message)


    def ConvertHTMLReversed(self, message):
        """ Converts some HTML reversed (&quot; &apos; etc...)
        message = The message you'd like to convert.
        Returns unicode string (even if message was str)
        (http://www.w3schools.com/tags/ref_entities.asp)
        """

        return self.HTMLParser.unescape(message)


    def HumanTime(self, dt, now=False):
        """ This function will return a string which will give a useful
        offset for humans ("5 minutes ago", "6 months ago", etc...):
        dt = datetime object
        now = the time you want to compare against (defaults to the time the function is called)
        
        Inspired by django (https://github.com/django/django/blob/master/django/utils/timesince.py)
        """
    
        if False == now:
            now = datetime.now()
        
        future = False

        if not isinstance(dt, datetime):
            raise TypeError("%s needs to be datetime instance")
        
        delta = (now - dt)
        delta = delta.days * 24 * 60 * 60 + delta.seconds
        
        if delta < 0:
            delta = -delta
            future = True

        for i, (seconds, singular, plural) in enumerate(self.time_units):
            count = delta // seconds # // operator does floor divison
            if count != 0:
                break
        if i >= 8 and delta < 60:
            if future:
                return "soon"
            else:
                return "just now"
        
        # currently fixed to english
        text = singular if count <= 1 else plural

        if future:
            return "in about %s" % (text % count)
        else:
            return "about %s ago" % (text % count)

    def convertToTime(self, ts):
        """
        This will convert a timestamp (ts) to a datetime object (what we use in MegBot)
        ts = float - comes from time.time()
        returns datetime.datetime

        """
        if type(ts) in [StringType]:
            ts = float(ts)
        return datetime.fromtimestamp(ts)


class L_Web(Standard):
    def __init__(self, connection):
        self.title = ""

    def WebSafeString(self, string):
        """
        Returns a web safe string to be put in urls (for GET requests).
        """
        return urllib.urlencode({"q":string})[2:]


    def SpellCheck(self, word):
        """ Uses googles spell checking capabilities
        returns corrected word (if there is one)
        word can be a string it'll be converted into websafe string.
        Will return -1 is an error occured!
        """
        try:
            g = urllib2.Request("http://google.com/search?q=%s" % self.WebSafeString(word))
            g.add_header("User-agent", "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16")
            g = urllib2.urlopen(g)
        except Exception:
            return -1
        d = g.read()
        if d.find("Showing results for </span>")!=-1:
            # Spelling correction :)
            correction = re.findall("<span class=\"spell\">Showing results for </span><a href=\"(.+?);spell=1\" class=spell>(.+?)<br>", d)
            if correction:
                correction = self.StripHTML(correction[0][1])
            else:
                correction = word
        else:
            correction = word
        return correction

class L_Format(Standard):
    """mIRC style formatting"""
    bold = chr(2)
    underline = chr(37)
    stress = chr(26)
    colour = chr(3)
    reset = chr(17)
    colours = {
        "white":"00",
        "black":"01",
        "blue":"02",
        "green":"03",
        "light red":"04",
        "brown":"05",
        "purple":"06",
        "orange":"07",
        "yellow":"08",
        "light green":"09",
        "cyan":"10",
        "light cyan":"11",
        "light blue":"12",
        "pink":"13",
        "grey":"14",
        "light grey":"15"
        }

    @staticmethod
    def _format(input, code):
        return "%s%s%s" % (code, input, code)

    @staticmethod
    def Bold(input):
        """Makes text bold"""
        return L_Format._format(input, L_Format.bold)

    @staticmethod
    def Stress(input):
        """Makes text stressed or italic (depending on the client)"""
        return L_Format._format(input, L_Format.stress)

    @staticmethod
    def Underline(input):
        """Makes text underlined"""
        return L_Format._format(input, L_Format.underline)

    @staticmethod
    def Colour(input, fcolour, bcolour=None):
        """Makes text coloured"""
        if bcolour == None:
            colour = fcolour
        else:
            colour = "%s,%s" % (fcolour, bcolour)

        return "%s%s%s%s" % (L_Format.colour, colour, input, L_Format.reset)

    @staticmethod
    def Reset(input):
        """Resets formatting"""
        return "%s%s" % (input, L_Format.reset)

class L_Channel(Standard):
    def __init__(self, connection, name):
        self.connection = connection # Connection of bot, instance.
        self.name = name
        self.topic = ""
        self.modes = []
        self.voiced = []
        self.ops = []
        self.halfops = []
        self.normals = []
        self.nicks = []
        for person in self.nicks:
            if person[0] in ["&", "~", "@"]:
                self.ops.append(erson[1:])
            elif person[0] == "%":
                self.halfops.append(person[1:])
            elif person[0] == "+":
                self.voiced.append(person[1:])
            else:
                self.users.append(person[1:])

        # Include all the nicks but with stripped off modes
        # e.g. &Jessica -> Jessica
        self.cleaned_nicks = self.ops + self.halfops + self.normals
        self.recently_sent = []
        self.recently_recved = []

    def __update_recently(self, message):
        self.recently_sent.append(message)
        if len(self.recently_sent) <= 5:
            self.recently_sent.pop(0)

    def format_message(self, message, args):
        """ Formats the message with args - ensuring everything is unicode """
        if args:
            args = tuple([unicode(arg) for arg in args])
            message = unicode(message) % args
        else:
            message = unicode(message)

        return message

    def send(self, message, *args):
        """Send PRIVMSG to channel"""
        message = self.format_message(message, args)
        self.connection.core["Coreprivmsg"].main(self.connection, self.name, message, True)
        self.__update_recently(message)

    def notice(self, message, *args):
        """Send NOTICE to channel"""
        message = self.format_message(message, args)
        self.connection.core["Corenotice"].main(self.connection, self.name, message)

    def action(self, message, *args):
        """Send a /me (CTCP ACTION)"""
        message = self.format_message(message, args)
        self.connection.core["Corectcp"].request(self.connection, self.name, message, "ACTION")

    def on_JOIN(self, connection, command):
        self.nicks.append(command.nick)
        self.normals.append(command.nick)


    def set_topic(self, topic, *args):
        message = self.format_message(message, args)
        self.topic = topic
        self.connection.server.raw("TOPIC %s :%s" % (self.name, topic))


    def voice(self, nick):
        if self.connection.server:
            self.connection.server.raw("MODE %s +v %s" % (self.name, nick))


    def devoice(self, nick):
        if self.connection.server:
            self.connection.server.raw("MODE %s -v %s" % (self.name, nick))


    def op(self, nick):
        if self.connection.server:
            self.connection.server.raw("MODE %s +o %s" % (self.name, nick))


    def deop(self, nick):
        if self.connection.server:
            self.connection.server.raw("MODE %s -o %s" % (self.name, nick))


    def set_mode(self, mode):
        if self.connection.server:
            self.connection.server.raw("MODE %s %s" % (self.name, mode))


    def on_MODE(self, connection, command):
        ## please re-write me O_o
        message = command.raw.split(" ")

        mode = message[3]
        if len(message) > 4:
            nick = message[4]
            def a(x, y):
                if x in self.normals:
                    self.normals.remove(x)
                y.append(x)
            def r(x, y):
                y.remove(x)
                if not (x in self.voiced or x in self.ops or self.halfops):
                    self.normals.append(x)
            if mode[0] == "-":
                func = r
            elif mode[1] == "+":
                func = a
            else:
                return
            # Now to check which mode...
            mode = mode[1:]
            for m in range(len(mode)):
                cm = mode[m] # current mode
                if cm.lower() == "o":
                    func(nick, self.ops)
                elif cm.lower() == "h":
                    func(nick, self.halfops)
                elif cm.lower() == "v":
                    func(nick, self.voiced)
        else:
            def r(x):
                if x in self.modes:
                    self.modes.remove(x)
            def a(x):
                if not x in self.modes:
                    self.modes.append(x)
            if mode[0] == "+":
                func = a
            elif mode [0] == "-":
                func = r
            else:
                return
            # Now check which mode...
            mode = mode[1:]
            for m in range(len(mode)):
                cm = mode[m]
                func(m)


    def on_TOPIC(self, connection):
        new_topic = command.message
        self.topic = new_topic


    def on_PRIVMSG(self, connection, command):
        self.recently_recved.append(command.message)
        if len(self.recently_recved) > 5:
            self.recently_recved.pop(0)


    def on_353(self, connection, command):
        ## looks buggy as hell, please fix.
        message = command.raw

        try:
            message = message[message.index(self.name)+1:]
        except ValueError:
            # Sometimes we get called for the wrong channel
            return
        message = message[0][1:] # ":" is put on the front of this.
        for n in message:
            self.nicks.append(n)
            if n[0] in ["&", "@", "~"]:
                self.ops.append(n[1:])
            elif n[0] == "%":
                self.halfops.append(n[1:])
            elif n[0] == "+":
                self.voiced.append(n[1:])
            else:
                self.normals.append(n)


    def on_332(self, connection, command):
        ## same as above, fix it!!!
        message = command.raw.split(" ")

        try:
            message = " ".join(message[message.index(self.name)+1:])[1:]
        except ValueError:
            # Sometimes we get called for the wrong channel
            return
        self.topic = message

class L_Server(Standard):
    def __init__(self, connection):
        self.connection = connection
        self.channels = self.connection.channels
        self.users = 0
        self.servers = 0
        self.channels = 0
        self.ops = 0
        self.motd = []
        self.nick = connection.settings["nick"]


    def raw(self, message, ending="\r\n"):
        """
        Sends a raw message, it appends the ending which defaults to
        \r\n, this will use the Core plugin Core/raw.py
        """
        self.connection.core["Coreraw"].main(self.connection, message, None, ending)


    def on_JOIN(self, connection, message):
        self.channels = self.connection.channels


    def send(self, nick, message=None):
        if not message:
            # Assumes it's a raw message
            self.connection.core["Coreraw"].main(self.connection, nick)
        else:
            self.connecton.core["Coreprivmsg"].main(self.conneciton, nick, message)


    def join(self, channel):
        self.connection.core["Corejoin"].main(self.connection, channel)


    def part(self, channel):
        # Core/part.py doesn't exist as isn't needed by the core of the
        # bot. so we're going to just part and clean it up.
        self.raw("PART %s" % channel)
        del self.connection.channels[channel]

        # need to figure out a way to unregister any still active hooks.



    def on_372(self, connection, command):
        self.motd.append(command.message[2:]) # for some reason they start with :-


    def nick(self, nick):
        # sets nickname
        self.connection.core["Coreraw"].main(self.connection, "NICK %s" % nick)
        self.connection.hooker.hook(self, "nick", nick)


    def on_NICK(self, connection, nick):
        self.nick = nick


    def mode(self, user, mode=None):
        if not mode:
            # Assumes user to be mode and it to be set on self
            mode = user
            user = self.nick
        self.raw("MODE %s %s" % (user, mode))


    def oper(self, user, password):
        self.raw("OPER %s %s" % (user, password))

    def away(self, reason=None):
        if reason == None:
            self.raw(":%s AWAY" % self.nick)
        else:
            self.raw("AWAY :%s" % reason)
