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

"""
"""

import traceback
from imp import load_source
from types import *
from threading import Timer

class Event(object):
    """Generic event class, doesn't do much without subclassing"""
    eventType = "Generic"

    def preInit(self, item, callback):
        pass

    def postInit(self, item, callback):
        pass

    def __init__(self, item, callback=None, eid=None):
        self.preInit(item, callback)

        self.item = item
        self.callback = callback
        self.eid = eid
        
        self.postInit(item, callback)

    def event(self, connection, event):
        if self.check(event):
            self.callback(connection, event.item)

    def preCheck(self, event):
        pass

    def check(self, event):
        self.preCheck(event)

        self.cresult = event == self.item
        
        self.postCheck(event)
        return self.cresult

    def postCheck(self, event):
        pass

    def destoryable(self, eid):
        if eid == self.eid:
            return True
        return False

    def deInit(self):
        pass

class TimedEvent(Event):
    """Timed event

    Creates a thread that sleeps for seconds, if the event is not unregistered
    then callback is called with args
    """
    eventType = "TIME"

    def __init__(self, seconds, callback=None, eid=None, args=[]):
        super(TimedEvent, self).__init__(seconds, callback, eid)

        self.thread = Timer(seconds, callback, args)
        self.thread.start()

    def deInit(self):
        self.thread.cancel()

    def event(self):
        """Dummy method, just to override parent's method"""
        pass

class IRCEvent(Event):
    """This is an IRC event

    No one knows how these things work. Just make a guess and hope.
    """
    eventType = "IRC"

    def check(self, event):
        # this really should be improved >.<
        self.preCheck(event)
        self.cresult = True

        ## need to check for all the attributes on Info object.
        remote = event.item
        citems = []

        for item in dir(self.item):
            if item.startswith("__"):
                # pass on magical methods/attributes
                continue
            attr = getattr(self.item, item)
            if not attr or type(attr) in [FunctionType, MethodType, UnboundMethodType]:
                # pass on functions and empty values
                continue

            citems.append((attr, getattr(remote, item)))

        for pear in citems:
            if pear[0] != pear[1]:
                self.cresult = False

        self.postCheck(event)
        return self.cresult


class Handler(object):
    def __init__(self, connection):
        self.connection = connection
        self.__events = {}
        
    def register_event(self, event):
        """ registers an event """
        if not event.eventType in self.__events:
            self.__events[event.eventType] = set()
        self.__events[event.eventType].add(event)

    def unregister_event(self, eid):
        """ Takes all events which have the id (eid) """
        new = {}
        for s in self.__events:
            new[s] = set()
            for e in self.__events[s]:
                if not e.destoryable(eid):
                    new[s].add(e)
                else:
                    e.deInit()
        self.__events = new 

    def event(self, event):
        """ passes an event off to all registered events """
        if event.eventType in self.__events:
            for e in self.__events[event.eventType]:
                e.event(self.connection, event)
