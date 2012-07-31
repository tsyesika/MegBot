# -*- coding: utf-8 -*-
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

import urllib2, re

def main(connection, line):
	if len(line.split()) <= 3:
		connection.core["privmsg"].main(connection, line.split()[2], "Please supply the word you want to be defined.")
		return
	st = "+".join(line.split()[4:])
	google = urllib2.Request("http://www.google.com/m?q=define+%s" % st)
	google.add_header("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3")
	google = urllib2.urlopen(google)
	source = google.read()
	pron = re.findall("<span class=\"t5vw2s\">(.+?)</span>", source)[0]
	if pron.replace("·", "").lower() == st.lower():
		correction = None
	else:
		correction = pron.replace("·�", "")
	chks = re.findall("<br/><span class=\"ut3asb\">(.+?):</span><span class=\"hxh2cq\">(.+?)</span>", source)
	if not chks:
		chks = re.findall("<span class=\"cg2aoo\">(.+?)\</span> <br/><span class=\"hxh2cq\">1. (.+?)</span>", source)
	if not chks:
		Channel.send("Sorry can't find definition for %s" % st)
		return 
	message = ""
	for x in chks:
		if x[0][0] == "(":
			x = (x[0].split("(")[1].split(")")[0], x[1])
		message += "| \002%s\017 - %s " % tuple(x)
	if correction:
		message += " (Corrected from: %s)" % st
	Channel.send(Helper.StripHTML("[%s] %s" % (pron, message[2:])))

help = "Uses google to define a word you specify"
