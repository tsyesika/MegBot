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

import urllib2, shelve, time
import xml.etree.ElementTree as etree

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
		different = "(Changed from: %s)" % " ".join(Info.args)
	else:
		different = ""
	
	# Lets replace , with +
	new_spelling = Web.WebSafeString(new_spelling)
	
	# first lets look up it's weoid.
	weoid = urllib2.urlopen("http://api.megworld.co.uk/WeoidLookup/lookup.php?place=%s&cache=1" % (new_spelling))
	weoid = weoid.read()
	if weoid == "Invalid." or not weoid:
		Channel.send("There has been a problem with the plugin. Please contact the developer.")
		return
	elif weoid == "Not Found":
		Channel.send("Can't find that place sorry. You sure it's spelt right? (%s)" % new_spelling.replace("+", " "))
		return

	cache = shelve.open("weather-cache")
	current_time = time.time()

	try:
		condition, wind, location, atmos, cache_time = cache[weoid]

		# check to see if cache is older than 1 hour
		if (current_time - cache_time) > 3600:
			raise KeyError #cheap hack :P

		print "Using cache for %s" % weoid

	except KeyError:
		# Either there's no cache or it's out of date
		# Let's lookup the weather using yahoo's weather API.
		weather = urllib2.urlopen("http://weather.yahooapis.com/forecastrss?w=%s" % weoid)
		weather = etree.fromstring(weather.read())

		# Grab XML elements from tree
		# (prefixes don't seem to be working in my version of python)
		condition = weather.find("channel/item/{http://xml.weather.yahoo.com/ns/rss/1.0}condition")
		wind = weather.find("channel/{http://xml.weather.yahoo.com/ns/rss/1.0}wind")
		atmos = weather.find("channel/{http://xml.weather.yahoo.com/ns/rss/1.0}atmosphere")

		# Location is given to us as in the form of city, region, country, but region
		# is sometimes "", so we do this:
		location = weather.find("channel/{http://xml.weather.yahoo.com/ns/rss/1.0}location")
		locate = []
		for i in ["city", "region", "country"]:
			tmp = location.get(i)
			if tmp:
				locate.append(tmp)
		location = ", ".join(locate)
		location = location.encode("utf-8") #quick hack in case of UNICODES :O
		location = Format.Bold(location)

		# Store weather in cache
		cache[weoid] = (condition, wind, location, atmos, current_time)
		cache.sync()
		cache.close()

	# Okay now we need to convert F to C & K
	c = int((float(condition.get("temp")) - 32) / (9 / 5.) + .5)
	k = c + 273
	
	# Convert wind speed from mph to kmph
	kmph = int(int(wind.get("speed")) * 1.60934 + .5)

	# Send it all to the channel
	Channel.send("[%s] Condition: %s | Temp: %sC/%sF/%sK | Humidity: %s%% | Wind Speed %smph/%skmph %s" % (location, condition.get("text"), c, condition.get("temp"), k, atmos.get("humidity"), wind.get("speed"), kmph, different))
	
help = "Uses Yahoo's weather API to give you the weather for the location specified."
