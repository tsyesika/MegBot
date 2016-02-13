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

from urllib2 import urlopen
import re
import json

def main(connection, info):
    if not info.args:
        info.channel.send("Please supply the word you want to be defined.")
        return

    query_original = " ".join(info.args)
    query_string = "+".join(info.args)

    url = "http://api.duckduckgo.com/?q=%s&format=json" % query_string
    request = urlopen(url)

    output = json.loads(request.read())

    if not 'Definition' in output or output['Definition'] == '':
        info.channel.send("Couldn't find a definition for %s", query_original)
    else:
        info.channel.send(u"[%s] %s",
            Format.Bold(query_original), 
            output['Definition']
        )

help = u"Use DuckDuckGo to define a word or phrase"
