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

import urllib2, urllib, re

def fixurl(url):
	url = url.replace("+", "%2B")
	url = url.replace("/", "%2F")
	url = url.replace("(", "%28")
	url = url.replace(")", "%29")
	url = url.replace(" ", "+")
	return url

def main(connection, line):
	if len(line.split()) <= 3:
		connection.core["privmsg"].main(connection, line.split()[2], "Plese enter mathamatical expression.")
		return
	exp = " ".join(line.split()[4:])
	google = urllib2.Request("http://google.com/m?q=%s" % fixurl(exp))
	google.add_header("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3")
	google = urllib2.urlopen(google)
	source = google.read()
	print source
	a = re.findall("<div class=\"wansgk\"><span class=\"sifhoi\">(.+?)</span> </div> <div>", source)
	try:
		connection.core["privmsg"].main(connection, line.split()[2], "%s" % a[0])
	except:
		connection.core["privmsg"].main(connection, line.split()[2], "Math Error: ?")
		
	