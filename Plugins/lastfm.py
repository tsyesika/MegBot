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

def main(connection):
    if not Info.args:
        user = Info.nick
    else:
        user = Info.args[0]
    try:
        #this key needs changing
        api_key = 'b25b959554ed76058ac220b7b2e0a026'
        url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=%s&api_key=%s&format=json"
        lastfm = urllib2.urlopen(url % (api_key, user))
        data = lastfm.read()
        data = json.loads(data)
        song = data[u'recenttracks'][u'track'][0]
        print song[u'artist'][u'name']
        Channel.send(u"%s is/was listening to: %s - %s", user, song[u'name'].encode('utf-8'), song[u'artist'][u'name'].encode('utf-8'))
    except Exception:
        Channel.send(u"Sorry there was an error, check your username?")

help = u"Gets the last scrobbled song from a specified user (if no one was specifies it tries your nick) from last.fm"
