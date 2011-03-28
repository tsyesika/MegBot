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

import urllib2, re, traceback

wind_direction = {
	"S":"South",
	"N":"North",
	"W":"West",
	"E":"East"
}
def main(connection, line):
	if len(line.split()) <= 3:
		connection.core["privmsg"].main(connection, line.split()[2], "Please supply a place you'd like the weather for.")
		return
	google = urllib2.urlopen("http://www.google.com/ig/api?weather=%s" % "+".join(line.split()[4:]).replace(",", ""))
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
		wind = re.findall("<wind_condition data=\"Wind: (.+?) at (.+?) mph\"/>", source)[0].replace(" ", "")
	except:
		wind = "N/A"
	try:
		wind = (wind[0], wind[1], int(wind[1]) * 1.609344)
	except:
		wind = (wind[0], wind[1], "N/A")
		traceback.print_exc()
	wd = []
	for d in range(len(wind[0])):
		wd.append(wind_direction[wind[0][d]])
	wd = " ".join(wd)
	connection.core["privmsg"].main(connection, line.split()[2], "%s: [Weather for %s]: \002Temp:\017 %s°C/%s°F/%s°K  \002Humidity:\017 %s%%  \002Wind Direction:\017 %s" % (line.split()[0][1:].split("!")[0], name, temp_c, temp_f, temp_k, humidity, wd))
	
def initalisation(connection):
	pass