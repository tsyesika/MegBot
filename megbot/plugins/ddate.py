##
#
# -*- coding: utf-8 -*-
#
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
##

from datetime import date
import calendar

DAYS = ["Sweetmorn", "Boomtime", "Pungenday", "Prickle-Prickle", "Setting Orange"]
SEASONS = ["Chaos", "Discord", "Confusion", "Bureaucracy", "The Aftermath"]
SEASONHOLIDAYS = ["Chaoflux", "Discoflux", "Confuflux", "Bureflux", "Afflux"]
APOSTLEHOLIDAYS = ["Mungday", "Mojoday", "Syaday", "Zaraday", "Maladay"]

def day_num(day):
    if day != 11 and ((day % 10) == 1):
        return str(day) + 'st'
    elif day != 12 and ((day % 10) == 2):
        return str(day) + 'nd'
    elif day != 13 and ((day % 10) == 3):
        return str(day) + 'rd'
    else:
        return str(day) + 'th'

def main(connection, info):
    today = date.today()
    is_leap_year = calendar.isleap(today.year)
    day_of_year = today.timetuple().tm_yday

    if is_leap_year and day_of_year >= 60:
        day_of_year -= 1

    season, day = divmod(day_of_year, 73)

    dayindex = (day_of_year - 1) % 5
    season = season % 4
    year = today.year + 1166
    output = "Today is %s, the %s day of %s in the YOLD %d."
    ndate = (DAYS[dayindex], day_num(day), SEASONS[season], year)

    if is_leap_year and today.month == 2 and today.day == 29:
        output = "Today is St. Tib's Day, YOLD %d" % year
    elif today.month == 3 and today.day == 25:
        output = (output % ndate) + " Don't Panic! Celebrate Towel Day!"
    elif day == 5:
        output = (output % ndate) + " Celebrate %s!" % APOSTLEHOLIDAYS[season]
    elif day == 50:
        output = (output % ndate) + " Celebrate %s!" % SEASONHOLIDAYS[season]
    else:
        output = output  % ndate
    info.channel.send(output)


help = u"Discordian Date, only return current date for now"
