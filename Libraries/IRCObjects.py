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

class Standard(object):
    """ Never instantiate """
    def __setuphooks__(self, connection):
        """ Sets up hooks for the class
        Any method on the class (inhereted) that begins with
        the prefix on_ will be automatically registered with
        the hooker
        """
        if "Corehooker" in connection.core.keys():
            # Woot, we got ability to have hooks
            for anm in dir(self):
                if anm.startswith("on_"):
                    connection.hooker.register_hook(anm, eval("self.%s" % anm))

class Info(Standard):
    def __init__(self, line=None):

        if line == None:
            # Make an empty Info.
            self.nick = ""
            self.ident = ""
            self.hostname = ""
            self.nickmask = tuple()
            self.parsed = tuple()
            self.action = ""
            self.raw = ""
            self.message = ""
            self.channel = ""
            self.plugin_name = ""
            self.trigger = ""
            self.args = []
            return

        ##
        # REMOVE me when this is being used properly.
        # (on close of #36)
        ##


        # Lets pull things out.
        self.raw = line
        self.parsed = self.parseIRC(line)
        
        if self.parsed and len(self.parsed) == 6:
            self.nickmask, self.action, self.channel, self.trigger, self.plugin_name, self.args = self.parsed
        elif self.parsed:
            self.nickmask, self.action, self.args = self.parsed
            self.channel, self.trigger, self.plugin_name = ("", "", "")
        else:
            return self.__init__(None)

        # Gets elements from nickmask
        if self.nickmask:
            self.nick, self.ident, self.hostname = self.nickmask
        else:
            self.nick, self.ident, self.hostname = ("", "", "")

        self.message = "%s%s %s" % (self.trigger, self.plugin_name, " ".join(self.args))

    def parseHostMask(self, nickmask):
        """ Parses the nickmask """
        if len(nickmask) <= 1:
            # can happen =[
            return ("", "", "")

        if "@" in nickmask:
            nickmask, host = nickmask.split("@", 1)
        else:
            host = ""

        if "!" in nickmask:
            nickname, ident = nickmask.split("!", 1)
            if ":" == nickname[0]:
                # why is this happening?
                nickname = nickname[1:]
        else:
            nickname, ident = ("", "")

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

        if ":" in message:
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

class L_Helper(Standard):
    def __init__(self):
        self.HTMLTagRe = re.compile(r'<[^<]+?>')
        self.HTMLParser = HTMLParser.HTMLParser()
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


    def TimeZoneCorrect(self, t, pre_timezone, post_timezone):
        """ This will convert from one timezone to another.
        t = time.time() - seconds after the EPOC
        pre_timezone = t is - +/-XXXX producable by time.strftime("%z")
        post_timezone = t should be in - UTC", "BST", etc..
                       producable by time.strftime("%Z")
        """

        utc = time.strptime(time.strftime("%b %d %H:%M:%S %Y ",
                                          time.gmtime(t))+pre_timezone,
                                          "%b %d %H:%M:%S %Y %Z")

        # convert to post_timezone
        et = time.strptime(time.strftime("%b %d %H:%M:%S %Y ",
                                          utc)+post_timezone,
                                         "%b %d %H:%M:%S %Y %Z")
        return ime.mktime(et)


    def HumanTime(self, t=time.time(), parse=None, f=None):
        """ This function will return a string which will give a useful
        offset for humans ("5 minutes ago", "6 months ago", etc...):
        t = time (float or string) froom time.time() or formatted (required)
        parse = a string for formatting
                    e.g. "%a %b %d %H:%M%S %Y %Z" (required if t is a str)

        f = from an offset, defaults to time.time() (now), must be a float.
        """

        if type(t) == type("") and parse:
            t = time.strptime(t, parse)
            t = time.mktime(t)
        else:
            t = float(t)
        # Find out time passed from now/f.
        if f:
            t = f-t
        else:
            t = time.time()-t
        # Work out time passed.
        if t < 60:
            return "Less than a minute"
        elif (t / 60) <= 60:
            # a hour
            m = int(t/60.0 + .5) # .5 to avoid floor rounding.
            if m <= 1:
                return "A minute"
            else:
                return "%s minutes" % m
        elif ((t / 60) / 60) <= 24:
            # a day
            h = int(t / 60.0 / 60.0 + 0.5)
            if h <= 1:
                return "A hour"
            else:
                return "%s hours" % h
        elif (((t / 60) / 60) / 24) <= 7:
            # a week
            d = int(t / 60.0 / 60.0 / 24.0 + 0.5)
            if d <= 1:
                return "A day"
            else:
                return "%s days" % d
        elif ((((t / 60) / 60) / 24) / 7) <= 4:
            # a month (29 days, lowest except 28)
            w = int(t / 60.0 / 60.0 / 24.0 / 7.0 + 0.5)
            if w <= 1:
                return "A week"
            else:
                return "%s weeks" % w
        elif (((t / 60) / 60) / 24) <= 365 :
            # a year
            m = int(t / 60.0 / 60.0 / 24.0 / 7.0 / 4.0 + 0.5)
            if m <= 1:
                return "A month"
            else:
                return "%s months" % m
        elif ((((t / 60) / 60) / 24) / 365) <= 10:
            # a decade (decade - century)
            y = int(t / 60.0 / 60.0 / 24.0 / 365.0 + 0.5)
            if y <= 1:
                return "A year"
            else:
                return "%s years" % y
        elif ((((t / 60) / 60) / 24) / 365) <= 100:
            # a century
            d = int(t / 60.0 / 60.0 / 24.0 / 365.0 / 10 + 0.5)
            if d <= 1:
                return "A decade"
            else:
                return "%s decades" % y
        else:
            c = int(t / 60.0 / 60.0 / 24.0 / 365.0 / 100.0 + 0.5)
            if c <= 1:
                return "A century"
            else:
                return "%s centuries" % c


class L_Web(Standard):
    def __init__(self, connection):
        self.title = ""
        self.HTMLTagRe = re.compile(r'<[^<]+?>')

    def StripHTML(self, text):
        """
        Strips HTML (also in Helper - subject to change).
        text is a string, will return it without any html elements.
        """
        return self.HTMLTagRe.sub("", text)


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
        except:
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

    def send(self, message):
        """Send PRIVMSG to channel"""
        self.connection.core["Coreprivmsg"].main(self.connection, self.name, message, True)
        self.__update_recently(message)

    def notice(self, message):
        """Send NOTICE to channel"""
        self.connection.core["Corenotice"].main(self.connection, self.name, message)

    def on_JOIN(self, connection, command):
        self.nicks.append(command.nick)
        self.normals.append(command.nick)


    def set_topic(self, topic):
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
