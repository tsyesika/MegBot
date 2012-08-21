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

import re, urllib2, shelve

def main(connection, line):
	#Checks to see if timezone is set :P
	userzones = shelve.open("TimeData")
	if len(Info.args) <= 1:
		if Info.nick in userzones.keys():
			sline.append(userzones[Info.nick])
		else:
			Channel.send("Please enter a location")
			return
	else:
		google = urllib2.Request("http://www.google.co.uk/search?q=time+%s" % Info.args[0].replace(" ", "%20"))
		google.add_header("User-Agent", "Mozilla/5.0 (compatible; U; Haiku x86; en-GB) AppleWebKit/536.10 (KHTML, like Gecko) Haiku/R1 WebPositive/1.1 Safari/536.10")
		google = urllib2.urlopen(google)
		source = google.read()
		try:
			time = re.findall("><td style=\"font-size:medium\"><b>(.+?)</b> (.+?) - <b>Time</b> in <b>(.+?)</b>", source)[0]
			Channel.send("Time: %s - %s - %s" % time)
		except:
			Channel.send("Sorry, couldn't retrive time.")
	userzones.sync()
	userzones.close()

help = "Uses google to look up the time, if no time is specified it will check to see if any time is save with it. Use -set <location> to set a location"
