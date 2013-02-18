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

"""This is handles all hooks, a hook is something which is called
but not by a direct user call. If a developer wants their code called
when a ping occurs, privmsg, join, part, etc... you use a hook. You can
only have one hook per function (i.e. you can't have the same function
called multiple times by a single line), this is ensured by the use of sets.

To register a hook you would use the register_hook method, unregistering you
call the unregister_hook method. To call all the hooks you make a call to hook
this will parse out the second element in the list (list[1]) and look
for all hooks which call on that.

The hooks should be registered with the prefix on_<hook> e.g. to
register on a PRVIMSG you would make a call to reigster:

    reigster_hook("on_PRIVMSG", <function>)

the capitalisation on the hook is important, the on_ should
be all lowercase with an uppercase hook (on_UPPERCASE).
The same is true for unregister_hook.

Hooks are not automatically unregistered, the onus is on the developer once
a hook is registerd for them to unregister it before their code is
unloaded/reloaded.
"""

import traceback
from imp import load_source

class Event():
    eventType = "Generic"

    def preInit(self, item, callback):
        pass

    def postInit(self, item, callback):
        pass

    def __init__(self, item, callback=None, eid=None):

        self.item = item
        self.callback = callback
        self.eid = eid
        
        self.postInit(item, callback)

    def event(self, event):
        if self.check(event):
            self.callback(event.item)

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

class IRCEvent(Event):
    eventType = "IRC"

    def check(self, event):
        # this really should be improved >.<
        for attr in dir(event.item):
            if attr.startswith("__"):
                continue
            try:
                remote = eval("event.item.%s" % attr)
                local = eval("self.item.%s" % attr)
                if remote and local:
                    if not remote == local:
                        return False 
            except:
                return False
        return True

class Handler():
    __events = {}

    def __init__(self):
        pass

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
                    new[s].add(event)
        self.__events = new 

    def event(self, event):
        """ passes an event off to all registered events """
        if event.eventType in self.__events:
            for e in self.__events[event.eventType]:
                e.event(event)
