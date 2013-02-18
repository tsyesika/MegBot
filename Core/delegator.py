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

    # can we make this better?
    command = connection.libraries["IRCObjects"].Info(command)

    if "PING" == command.action:
        # Lets hand off to ping in case it's a PING message.
        connection.core["Coreping"].main(connection, command)

    # Okay, we'll now see if any hooks wish to be called on it.
    connection.hooker.hook(connection, command)

    if not command.message:
        return

    trigger = connection.settings["trigger"]
    if command.trigger != trigger:
        return

    # Okay so at this point we can say they are trying to call a plugin.
    # first thing's first is we need to check the plugin actually exists

    if command.plugin_name not in connection.plugins:
        return

    # last thing we need to do is delegate off to the executor core plugin
    # this will put the plugin into a thread and execute it.
    ##
    # Remove .split() when #36 is done
    ##
    connection.core["Coreexecutor"].main(connection, command.raw.split(), command.plugin_name)
