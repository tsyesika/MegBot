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

import urllib2, re, time, traceback

wind_direction = {
	"S":"South",
	"N":"North",
	"W":"West",
	"E":"East",
	"NW":"North West",
	"SW":"South West",
	"NE":"North East",
	"SE":"South East"
}
def main(connection, line, url=None, tag=""):
	# to do - use a proper parsing technique (regex = baddd)
	if len(line.split()) <= 3:
		Channel.send("Please supply a place you'd like the weather for.")
		return
	if not url:
		google = urllib2.urlopen("http://www.google.com/ig/api?weather=%s" % "+".join(line.split()[4:]).replace(",", ""))
	else:
		google = urllib2.urlopen(url)
	source = google.read()
	try:
		name = re.findall("><city data=\"(.+?)\"/>", source)[0]
	except:
		name = " ".join(line.split()[4:])
	try:
		current = re.findall("<current_conditions><condition data=\"(.+?)\"/<temp_f", source)[0]
	except:
		current = "N/A"
	try:
		temp_f = re.findall("<temp_f data=\"(.+?)\"/><temp_c", source)[0]
	except:
		temp_f = "N/A"
	try:
		temp_c = re.findall("<temp_c data=\"(.+?)\"/><humidity", source)[0]	
	except:
		temp_c = "N/A"
	try:
		temp_k = 273 + int(temp_c)
	except:
		temp_k = "N/A"
	try:
		humidity = re.findall("<humidity data=\"Humidity: (.+?)%\"/><icon", source)[0]
	except:
		humidity = "N/A"
	try:
		wind = re.findall("<wind_condition data=\"Wind: (.+?) at (.+?) mph\"/>", source)[0]
	except:
		wind = "N/A"
	try:
		wind = (wind_direction[wind[0]], wind[1], int(int(wind[1]) * 1.609344))
	except:
		wind = ("N/A", "N/A", "N/A")
	if temp_c == "N/A" and temp_f == "N/A" and temp_k == "N/A" and humidity == "N/A":
		#Checks to see if spelt wrong..
		lu = urllib2.urlopen("http://google.com/m/?q=weather+%s" % "+".join(line.split()[4:]).replace(",", ""))
		lu = lu.read()
		if lu.find("<br/> Showing results for  <a href=")!=-1:
			print 1
			cname = re.findall("<br/>  <br/> Showing results for  <a href=\"(.+?)\">(.+?) </a>. Search inste", lu)[0][1].replace(" ", "+")
			main(connection, line, "http://www.google.com/ig/api?weather=%s" % cname, "(Corrected to %s from %s)" % (" ".join(cname.split("+")[1:]), " ".join(line.split()[4:])))
			return
		else:
			Channel.send("%s: Couldn't get data for %s" % (line.split()[0][1:].split("!")[0], name))
	else:
		Channel.send("%s: [Weather for %s]: \002Temp:\017 %s°C/%s°F/%sK  \002Humidity:\017 %s%%  \002Wind Direction:\017 %s  \002Wind Speed:\017 %smph/%skph %s" % (line.split()[0][1:].split("!")[0], name, temp_c, temp_f, temp_k, humidity, wind[0], wind[1], wind[2], tag))

help = "Uses google to try and look up a weather from a specified place."
