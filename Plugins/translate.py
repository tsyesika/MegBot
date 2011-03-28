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

import urllib2, re, traceback

def main(connection, line):
	if len(line.split()) <= 3:
		connection.core["privmsg"].main(connection, line.split()[2], "Please supply lang|lang <text to translate> or languages")
		return
	if line.split()[4] == "languages":
		pass
	else:
		if line.split()[4].find("|")!=-1:
			#pipe used
			langpair = (line.split()[4].split("|")[0], line.split()[4].split("|")[1])
		else:
			langpair = ("auto", line.split()[4])
		try:
			google = urllib2.Request("http://translate.google.com/?text=%s&sl=%s&tl=%s" % ("+".join(line.split()[5:]), langpair[0], langpair[1]))
			google.add_header("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3")
			google = urllib2.urlopen(google)
			source = google.read()
			langtran = re.findall("<h3 id=headingtext class=\"\">(.+?) to (.+?) translation</h3>", source)[0]
			result = re.findall("onmouseout=\"this.style.backgroundColor='#fff'\">(.+?)</span></span></div></div><di", source)[0]
			connection.core["privmsg"].main(connection, line.split()[2], "%s: \002[%s to %s]\017 %s" % (line.split()[0][1:].split("!")[0], langtran[0], langtran[1], result))
		except:
			traceback.print_exc()

def initalisation(connection):
	pass
	