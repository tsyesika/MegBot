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
	"""
	Uses the Yahoo API with the (so far) undocumented Weoid API MegWorld provides.
	This will check the spelling of the entered place, look up it's Weoid and then the weather for said place.
	The Yahoo weather documentation is:
	http://developer.yahoo.com/weather/
	The MegWorld Weoid API takes the argument place as a GET argument.
	
	Todo:
	- Speed improvements? (possibly add caching?)
	"""
	if not Info.args:
		Channel.send("Please specify a place")
		return
	
	# Checks the spelling of said place.
	new_spelling = Web.SpellCheck(" ".join(Info.args))
	different = False
	if new_spelling != " ".join(Info.args):
		# They're different (lets add (corrected from onto it))
		different = "(Changed from: %s" % " ".join(Info.args)
	else:
		different = ""
	
	# Lets replace , with +
	new_spelling = new_spelling.replace(",", "+")
	new_spelling = new_spelling.replace(";", "+")
	new_spelling = new_spelling.replace(".", "")
	
	# first lets look up it's weoid.
	weoid = urllib2.urlopen("http://api.megworld.co.uk/WeoidLookup/lookup.php?place=%s" % ("+".join(new_spelling.split())))
	weoid = weoid.read()
	if weoid == "Invalid.":
		Channel.send("There has been a problem with the plugin. Please contact the developer.")
		return
	elif weoid == "Not Found":
		Channel.send("Can't find that place sorry. You sure it's spelt right? (%s)" % new_spelling)
		return
	
	# Okay dokie, lets now lookup the weather using yahoo's weather API.
	weather = urllib2.urlopen("http://weather.yahooapis.com/forecastrss?w=%s" % weoid)
	weather = weather.read()
	
	at = re.findall("<yweather:atmosphere humidity=\"(.+?)\"  visibility=\"(.+?)\"  pressure=\"(.+?)\"  rising=", weather)[0]
	cond = re.findall("<yweather:condition  text=\"(.+?)\"  code=\"(.+?)\"  temp=\"(.+?)\"  date=", weather)[0]
	wind = re.findall("<yweather:wind chill=\"(.+?)\"   direction=\"(.+?)\"   speed=\"(.+?)\" />", weather)[0]
	
	# okay now we need to convert F to C & K
	c = int((float(cond[2]) - 32) / (9 / 5.) + .5)
	k = c + 273
	
	# Convert wind speed from mph to kmph
	kmph = int(int(wind[2]) * 1.60934 + .5)
	
	location = re.findall("<title>Yahoo! Weather - (.+?)</title>", weather)[0]
	
	Channel.send("[%s] Condition: %s | Temp: %sC/%sF/%sK | Wind Speed %smph/%skmph %s" % (location, cond[0], c, cond[2], k, wind[2], kmph, different))
	
help = "Uses Yahoo's weather API to give you the weather for the location specified."
