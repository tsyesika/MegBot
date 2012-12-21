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

import urllib2, re, json

def main(connection):
    if not Info.args:
        Channel.send("Please supply the word you want to be defined.")
        return
    query_original = " ".join(Info.args)
    query_string = "+".join(Info.args)
    request = urllib2.urlopen("http://api.duckduckgo.com/?q=define+%s&format=json" % query_string)

    output = json.loads(request.read())
    if output['AbstractText'] == '':
        Channel.send("Couldn't find a definition for %s" % query_original)
    else:
        Channel.send("[%s] %s" % (Format.Bold(query_original), output['AbstractText']))

help = "Use DuckDuckGo to define a word or phrase"
