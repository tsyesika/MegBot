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
from urllib import quote

def main(connection, info):
    if not info.args:
        info.channel.send(u"Please supply the word you want to be defined.")
        return
    urbanterm = quote(' '.join(Info.args))
    google = urllib2.Request("http://www.urbandictionary.com/define.php?term=%s" % urbanterm)
    google.add_header("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3")
    try:
        google = urllib2.urlopen(google)
    except Exception:
        info.channel.send(u"Cannot access urbandictionary.com")
        return
    source = google.read()
    try:
        name = String(re.findall("<td class='word'>\n<span>\n(.+?)\n</span>", source)[0])
        definition = String(re.findall("<div class=\"definition\">(.+?)</div><div", source)[0])
        definition = u"%s: [%s] - %s" % (info.nick, Format.Bold(name), Helper.ConvertHTMLReversed(definition))
    except Exception:
        definition = u"Sorry, can't find a definiton"
        traceback.print_exc()
    info.channel.send(Helper.ConvertHTMLReversed(Helper.StripHTML(definition)))

help = u"Tries to pull a definition from urbandictionary.com"
