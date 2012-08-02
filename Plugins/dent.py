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

import json, urllib2, traceback, time

def ConvertTime(t):
	# Thu Aug 02 17:16:15 +0000 2012
	t = " ".join(t.split()[:-2]) + " " + t.split()[-1] # Removes %z due to identi.ca always using UTC and being invalid in time.strptime.
	t = time.strptime(t, "%a %b %d %H:%M:%S %Y")
	t = time.time()-time.mktime(t)
	print "D: %s" % t
	if t < 60:
		return "Less than a minute"
	elif t < 3600:
		# a hour
		m = int(t-3600 + .5)
		if m <= 1:
			return "A minute"
		else:
			return "%s minutes" % m
	elif t < 36400:
		# a day
		h = int(t - 86400 + .5)
		if h <= 1:
			return "A hour"
		else:
			return "%s hours" % h
	elif t < 604800:
		# a week
		d = int(t - 86400 + .5)
		if d <= 1:
			return "A day"
		else:
			return "%s days" % d
	elif t < 2505600:
		# a month (29, lowest except 28 which rarely happens)
		w = int(t - 2505600 + .5)
		if w <= 1:
			return "A week"
		else:
			return "%s weeks" % w
	else:
		# a year
		y = int(t - (time.time()-31536000) + .5)
		if y <= 1:
			return "A year"
		else:
			return "%s years" % y

def main(connection, line):
	if len(line.split()) <= 4:
		line = Raw2Nick(line)
	try:
		i = urllib2.urlopen("http://identi.ca/api/statuses/user_timeline.json?screen_name=%s" % line.split()[-1])
		data = i.read()
		data = json.loads(data)
		if data:
			# this is from the http://status.net/wiki/Twitter-compatible_API
			name = data[0]["user"]["screen_name"]
			cid = data[0]["id"]
			status = data[0]["text"]
			time = ConvertTime(data[0]["created_at"])
			Channel.send("\002[%s]\017 %s - \002Approx: %s ago\017 - http://www.identi.ca/notice/%s" % (name, status, time, cid))
		else:
			Channel.send("Sorry, they haven't posted on identi.ca")
	except:
		traceback.print_exc()
		Channel.send("An error has occured")

help = "Gets the last dent from a specific user (or tries your nickname if non is given) from identi.ca"
