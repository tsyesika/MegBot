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
import hashlib
import os
import socket
import types

def mock_closure(keeper):
    """ Fake closure which is used when
    non if given
    """
    return

class Keeper():
    bot = None
    never = None

    def __init__(self, item=None, expire=None, closure=None):
        """ Sets up inital variables """
        if not self.bot:
            # this should have been set, this class won't function
            # correctly without a link with the bot.
            raise Exception

        self.item = item
        self.time = time.time()
        # this doesn't need to be secure but it does need to be fast.
        self.id = hashlib.sha1(self.item.__str__ + os.urandom(10))
        self.expire = expire
        if closure == None:
            self.closure = mock_closure
        else:
            self.closure = closure

    def expire():
        """ Will expire item """
        self.__wrapup()
        self.__destrory()

    def changeExpirery(expire):
        """ Will change the time which the item expires """
        self.expire = expire

        # Now lets check if it's expired.
        if self.__checkExpired():
            # wrap up
            self.__wrapup()
            
            # now lets destory it.
            self.__destrory()

    def __wrapup(self):
        """ Wraps up the things needed """
        if type(self.item) == type(socket.socket()):
            # It's a socket
            self.closure(self)

            # Now close
            try:
                self.item.close()
            except socket.error:
                # what happened, should i be catching this? :s
                # closing a closed socket doesn't cause an exception
                pass

        elif type(self.item) == types.FileType:
            # Okay so it's a file
            self.closure(self)

            # Now close it
            if not self.item.closed:
                self.item.close()

        # what else could it be?

    def __destroy():
        """ Destorys self """
        self.bot.unregister(self.id)
