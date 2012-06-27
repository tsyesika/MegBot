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

import urllib2, json

def main(connection, line):
	if len(line.split()) <= 3:
		user = line.split()[0].split("!")[0][1:]
	else:
		user = line.split()[4]
	try:
		lastfm = urllib2.urlopen("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=b25b959554ed76058ac220b7b2e0a026&format=json" % user)
		data = lastfm.read()
		data = json.loads(data)
		song = data[u'recenttracks'][u'track'][0]
		Channel.send("%s is/was listening to: %s - %s" % (user, song[u'name'].encode('utf-8'), song[u'artist'][u'#text'].encode('utf-8')))
	except:
		Channel.send("Sorry there was an error, check your username?")
