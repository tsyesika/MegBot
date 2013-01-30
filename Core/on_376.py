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

"""This is called at the end of MOTD.
We want to send the nickserv and join commands when we've connected
to the network. If you send them before the MOTD has finished then
some IRCd's will ignore them completely resulting in a valid identifcation
message which has been sent not being achologed or acted on.

Todo: allow the sleep to defined in the config (possibly like irssi 'wait 2000')
"""

import time

def main(connection, message):
    """End of MOTD"""

    if connection.settings["modes"]:
        connection.core["Coreraw"].main(connection,
                                        "MODE %s %s" %
                                            (
                                            connection.settings["nick"],
                                            connection.settings["modes"]
                                            )
                                        )

    if connection.settings["NSPassword"]:
        prvmsg = connection.core["Coreprivmsg"].main
        prvmsg(connection,
               "NickServ",
               "identify %s" % (
                               connection.settings["NSPassword"]
                               )
              )

    for channel in connection.settings["channels"]:
        connection.core["Corejoin"].main(connection, channel)

    time.sleep(2)

    for cmd in connection.settings["commands"]:
        connection.core["Coreraw"].main(connection, cmd)
