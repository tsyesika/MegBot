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

import json, urllib2, traceback

def main(connection, line):
	if not Info.args:
		line = line + " " + Info.args[0]
	try:
		i = urllib2.urlopen("http://twitter.com/statuses/user_timeline/%s.json?callback=twitterCallback2&count=1" % line.split()[-1])
		data = i.read()
		data = json.loads(data[17:-2])
		if data:
			name = data[0]["user"]["screen_name"]
			cid = data[0]["id"]
			status = data[0]["text"]
			time = data[0]["created_at"]
			Channel.send("[%s] %s " % (Format.Bold(name), status))
		else:
			Channel.send("Sorry, they haven't tweeted")
	except:
		traceback.print_exc()
		Channel.send("An error has occured")

help = "Tries to find the last tweet by specified user, if no one specified tries to use your nickname"
