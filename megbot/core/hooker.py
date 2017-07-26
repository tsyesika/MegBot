##
# This file is part of MegBot.
#
# MegBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MegBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MegBot. If not, see <http://www.gnu.org/licenses/>.
##

from types import *

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

class Hooker(object):
    """Deals with the MegBot hooks system"""
    __hooks = {}

    def copy(self, orig):
        """ Produces a deep copy of orig """
        new = []
        for elem in orig:
            if type(elem) == ListType:
                new.append(self.copy(elem))
            else:
                new.append(elem)
        return new

    def __init__(self):
        self.register_hook('on_376', load_source("on_376",
                                                 "megbot/core/on_376.py").main)
        self.register_hook('on_422', load_source("on_376",
                                                 "megbot/core/on_376.py").main)
        self.register_hook('on_QUIT', load_source("on_QUIT",
                                                  "megbot/core/on_QUIT.py").main)
        self.register_hook('on_JOIN', load_source("on_QUIT",
                                                  "megbot/core/join.py").on_JOIN)
        self.register_hook('on_396', load_source("on_396",
                                          "megbot/core/on_396.py").main)
    
    def hook(self, bot, command):
        """Hooks plugins, etc..."""
        print "[IN] %s" % command.raw

        act = 'on_%s' % command.action
        if act not in self.__hooks.keys():
            return
        
        try:
            hooks = self.copy(self.__hooks[act])
            for callback in hooks:
                callback(bot, command)
        except Exception:
            print "[ErrorLine] %s" % command.raw
            traceback.print_exc()

    def register_hook(self, hook, callback):
        """registers a new callback"""
        if hook not in self.__hooks.keys():
            self.__hooks[hook] = set()
        self.__hooks[hook].add(callback)

    def unregister_hook(self, hook, callback):
        """unregisters an existing callback"""
        if hook in self.__hooks.keys():
            self.__hooks[hook].remove(callback)
