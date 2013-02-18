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

import urllib2, re

USER_AGENT = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3"

def main(connection):
    if not Info.args:
        Channel.send("Please supply the word you want to be defined.")
        return
    phrase = "+".join(Info.args)
    google = urllib2.Requephrase("http://www.google.com/m?q=define+%s" % phrase)
    google.add_header("User-Agent", USER_AGENT)
    google = urllib2.urlopen(google)
    source = google.read()
    pron = re.findall("<span class=\"t5vw2s\">(.+?)</span>", source)[0]
    if pron.replace("·", "").lower() == phrase.lower():
        correction = None
    else:
        correction = pron.replace("·�", "")
    chks = re.findall("<br/><span class=\"ut3asb\">(.+?):</span><span class=\"hxh2cq\">(.+?)</span>", source)
    if not chks:
        chks = re.findall("<span class=\"cg2aoo\">(.+?)\</span> <br/><span class=\"hxh2cq\">1. (.+?)</span>", source)
    if not chks:
        Channel.send("Sorry can't find definition for %s" % phrase)
        return
    message = ""
    for part in chks:
        if part[0][0] == "(":
            part = (part[0].split("(")[1].split(")")[0], part[1])
        message += "| %s - %s " % (Format.Bold(part[0]), part[1])
    if correction:
        message += " (Corrected from: %s)" % phrase
    Channel.send(Helper.StripHTML("[%s] %s" % (pron, message[2:])))

help = "Uses google to define a word you specify"
