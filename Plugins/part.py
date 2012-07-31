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

def main(connection, line):
	if len(line.split()) <= 3:
		connection.core["raw"].main(connection, "PART %s" % line.split()[2])
		return
	connection.core["raw"].main(connection, "PART %s" % line.split()[4])
	Channel.send("Parted from %s." % line.split()[4])

help = "Parts from a specified channel"
