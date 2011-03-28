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

import re, urllib2

def main(connection, line):
	if len(line.split()) <= 3:
		connection.core["privmsg"].main(connection, line.split()[2], "Please enter a location")
		return
	google = urllib2.Request("http://www.google.com/search?q=time+%s" % line.split()[4].replace(" ", "%20"))
	google.add_header("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3")
	google = urllib2.urlopen(google)
	source = google.read()
	try:
		time = re.findall("><td style=\"font-size:medium\"><b>(.+?)</b> (.+?) - <b>Time</b> in <b>(.+?)</b>", source)[0]
		connection.core["privmsg"].main(connection, line.split()[2], "Time: %s - %s - %s" % time)
	except:
		connection.core["privmsg"].main(connection, line.split()[2], "Sorry, couldn't retrive time.")
		
def initalisation(connection):
	pass