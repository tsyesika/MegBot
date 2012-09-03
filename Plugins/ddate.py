##
#   This file is part of MegBot
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
#   
# -*- coding: utf-8 -*-
##

from datetime import date
import calendar

def DayNum(day):
	if day!=11 and ((day % 10) == 1):
		return `day` + 'st'
	elif day!=12 and ((day % 10) == 2):
		return `day` + 'nd'
	elif day!=13 and ((day % 10) == 3):
		return `day` + 'rd'
	else:
		return `day` + 'th'

def main(connection, line):
	seasons = ["Chaos", "Discord", "Confusion", "Bureaucracy", "The Aftermath"]
	days = ["Sweetmorn", "Boomtime", "Pungenday", "Prickle-Prickle", "Setting Orange"]
	seasonholidays = ["Chaoflux", "Discoflux", "Confuflux", "Bureflux", "Afflux"]
	apostleholidays = ["Mungday", "Mojoday", "Syaday", "Zaraday", "Maladay" ]
	today = date.today()
	is_leap_year = calendar.isleap(today.year)
	day_of_year = today.timetuple().tm_yday

	if is_leap_year and day_of_year >= 60:
		day_of_year -= 1

	season, day = divmod(day_of_year, 73)

	dayindex = (day_of_year - 1) % 5
	season = season % 4
	year = today.year + 1166
	if is_leap_year and today.month == 2 and today.day == 29:
		ddate = "Today is St. Tib's Day, YOLD %d" % year
	elif today.month == 3 and today.day == 25:
		ddate = "Today is %s, the %s day of %s in the YOLD %d. Don't Panic! Celebrate: Towel Day!" % (days[dayindex], DayNum(day), seasons[season], year)
	elif day == 5:
		ddate = "Today is %s, the %s day of %s in the YOLD %d. Celebrate: %s!" % (days[dayindex], DayNum(day), seasons[season], year, apostleholidays[season])
	elif day == 50:
		ddate = "Today is %s, the %s day of %s in the YOLD %d. Celebrate: %s!" % (days[dayindex], DayNum(day), seasons[season], year, seasonholidays[season])
	else:
		ddate = "Today is %s, the %s day of %s in the YOLD %d." % (days[dayindex], DayNum(day), seasons[season], year)
	Channel.send(ddate)
	

help = "Discordian Date, only return current date for now"
