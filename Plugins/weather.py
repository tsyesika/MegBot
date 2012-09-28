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
	Uses googles page to parse out weather and display it.
	This plugin might be better relying or at least having a fall back situation on a
	constant API as google seem to enjoy wapping their code around so this method
	breaks frequently. Yet to find a good API though. Also maybe look into some HTML parser
	or write one instead of using ugly regexes
	"""
	if not Info.args:
		Channel.send("Please specify a place")
		return
	
	# Checks the spelling of said place.
	new_spelling = Web.SpellCheck(" ".join(Info.args))
	different = False
	if new_spelling != " ".join(Info.args):
		# They're different (lets add (corrected from onto it))
		different = True
	else:
		new_spelling = " ".join(Info.args)
	
	g = urllib2.Request("http://google.co.uk/search?q=weather+%s" % Web.WebSafeString(new_spelling))
	g.add_header("User-agent", "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16")
	try:
		g = urllib2.urlopen(g)
		d = g.read()
	except:
		Channel.send("There was a fault connecting with the weather server. Please try later")
		return
	
	if d.find("<span class=\"vk_h\">")==-1:
		Channel.send("Can't find any weather for that location. Sorry")
		return

	place = re.findall("<span class=\"vk_h\">(.+?)</span><div class=\"vk_sh\" styl", d)[0]
	conditions = re.findall(", </span><span id=\"wob_dc\">(.+?)</span></div></div>", d)[0]
	temp = re.findall("<span class=\"wob_t wob_ct vk_bk\" id=\"wob_tm\">(.+?)</span><span class=\"wob_t vk_bk\" id=\"wob_ttm\" style=\"display:(.+?)\">(.+?)</span></div>", d)[0]
	temp = (int(temp[0]), int(temp[2]), int(temp[0]) + 273)
	precip = re.findall("<div>Precip:&nbsp;<span id=\"wob_pp\">(.+?)</span></div><div>", d)[0]
	humidity = re.findall("</div><div>Humidity:&nbsp;<span id=\"wob_hm\">(.+?)</span>", d)[0]
	ws = re.findall("<span><span class=\"wob_t\" id=\"wob_ws\" style=\"display:(.+?)\">(.+?)</span>", d)[0][1]
	if ws.endswith("km/h"):
		ws = "%s mph/%s" % (int(int(ws.split()[0])*0.621371 + .5), ws)
	else:
		ws += "/%s km/h" % (int(int(ws.split()[0])*1.60934 + .5)) 
	Channel.send("[%s] Condition: %s | Temp: %s°C/%s°F/%sK | Precpitation: %s | Humidity: %s | Wind Speed: %s" % (place, conditions, temp[0], temp[1], temp[2], precip, humidity, ws))
	
	
help = "Uses google to try and look up a weather from a specified place."
