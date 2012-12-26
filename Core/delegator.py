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

"""This will handle the validation and delegation of IRC messages.
it'll always return None (even if it's valid), it'll first validate
the message once it has, it'll check to see a plugin should be called.
If a plugin should be called i.e.

  nick!ident@host PRIVMSG #channel :<trigger><valid plugin>[args]

then it'll delegate that to the core executor plugin.
"""

def main(connection, command):
    """Delegates to other other core items when a valid IRC command 
    is passed to it.

    command: this should be a raw command passed from the IRCd (str)

    e.g.
        PING :gilman.megworld.co.uk
        nick!ident@host PRIVMSG #megworld :this is a message.

    the function will return None as it'll delegate to other core
    modules or do nothing and return back.
    """
    
    # we don't want to do anything if the line is blank
    if not command:
        return

    # since we want to look at each element we'll split it
    # it'll be quicker splitting it once here than each time
    # we want to examen an element. Splitting it by spaces.
    split_command = command.split()


    # We need to know the length for some inital crude validation
    # since like split we need locations we'll calculate it once.
    split_length = len(split_command)

    
    # Lets hand off to ping in case it's a PING message.
    connection.core["Coreping"].main(connection, split_command)
    

    # Okay, if it's short than length one it's ether a ping (which
    # has been handled now) or it's malformed in which case we don't
    # want to do anything more with it so we'll end here.
    if split_length <= 1:
        return

    # Okay, we'll now see if any hooks wish to be called on it.
    connection.hooker.hook(connection, split_command[1], command)

    # Now we just need to handle plugin calls, these will always be
    # like ["nick!ident@host", "PRIVMSG", "#channel", ":message"]
    # so minimum length will be 4 for a valid message.
    # any messages less than or equal to 3 in length or if the
    # type isn't a PRIVMSG then we can ignore the command

    if split_length <= 3 or split_command[1] != "PRIVMSG":
        return

    # Now we'll check the line isn't blank
    # a blank line will look like:
    # ["nick!ident@host", "PRIVMSG", "#channel", ":"]
    # if it's blank we can throw it away.
    
    if split_command[3] == ":":
        return

    # Okay now we need to test that the trigger has been used
    # if it has we know the user is trying to execute a plugin.
    # First triggers could be bigger than 1 character so lets get 
    # the length of the trigger.

    trigger = connection.settings["trigger"]
    trigger_length = len(trigger)
    
    # if they didn't use the trigger, we can do nothing.
    
    if split_command[3][1:trigger_length+1] != trigger:
        return

    # Okay so at this point we can say they are trying to call a plugin.
    # first thing's first is we need to check the plugin actually exists
    
    plugin = split_command[3][trigger_length+1:]
    if plugin not in connection.plugins:
        return

    # last thing we need to do is delegate off to the executor core plugin
    # this will put the plugin into a thread and execute it.

    connection.core["Coreexecutor"].main(connection, command, plugin)
