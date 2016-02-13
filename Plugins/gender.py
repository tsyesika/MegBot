##
#This file is part of MegBot.
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

import urllib2

DEFINITIONS = {
    "F":"female",
    "M":"male",
    "U":"unisex"
}

def main(connection, info):
    # Find name
    if not info.args:
        Channel.send("Please specify a name.")
        return

    name = info.args[0]

    reply = urllib2.urlopen("http://api.megworld.co.uk/Name-Gender/gender.php?name=%s" % name)
    reply = reply.read()
    if reply in DEFINITIONS.keys():
        info.channel.send("%s is %s" % (name, DEFINITIONS[reply]))
    else:
        info.channel.send("Sorry we don't know %s, please check later for it" % name)

help = "Uses MegWorld's API to try and work out the gender from a given real name"
