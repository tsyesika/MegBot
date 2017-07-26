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

"""This will send a notice to the IRCd."""

def main(connection, channel, message):
    """ Sends a NOTICE """

    message = "NOTICE %s :%s" % (channel, message)

    # Max length of message can be 510
    # (512 inc. \r\n so 510 as raw adds those).
    # See section 2.3 of RFC1459
    if len(message) > 510:
        print "[ERRORLINE] Next NOTICE will get truncated!"
    connection.core["Coreraw"].main(connection, message)
