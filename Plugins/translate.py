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

supported = ["en", "de", "cy", "af", "sq", "ar", "hy", "az", "eu", "be", "bn", "bg", "ca", "zh-CN", "zh-TW", "hr", "cs", "da", "nl", "et", "tl", "fi", "fr", \
			"gl", "ka", "de", "el", "gu", "ht", "iw", "hi", "hu", "is", "id", "ga", "it", "ja", "kn", "ko", "la", "lv", "lt", "mk", "ms", "mt", "no", "fa", \
			"pl", "pt", "ro", "ru", "sr", "sk", "sl", "es", "sw", "sv", "ta", "te", "th", "tr", "uk", "ur", "vi", "yi"]

# This is the default language if no language is specified (languages which can be default languages arei n supported)
default_language = "en"

def main(connection, line):
	if len(line.split()) <= 3:
		Channel.send("Please supply lang|lang <text to translate> or languages")
		return
	if line.split()[4] == "languages":
		pass
	else:
		if line.split()[4].find("|")!=-1:
			#pipe used
			langpair = (line.split()[4].split("|")[0], line.split()[4].split("|")[1])
			ltranslate = "+".join(line.split()[5:])
		else:
			if line.split()[4] in supported:
				langpair = ("auto", line.split()[4])
				ltranslate = "+".join(line.split()[5:])
			else:
				langpair = ("auto", default_language)
				ltranslate = "+".join(line.split()[4:])
		try:
			# Bug detection faulty
			google = urllib2.Request("http://translate.google.com/m?sl=%s&tl=%s&ie=UTF-8&prev=_m&q=%s" % (langpair[0], langpair[1], ltranslate))
			google.add_header("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3")
			google = urllib2.urlopen(google)
			source = google.read()
			langtran = re.findall("lass=\"s1\">(.+?)</a>.*>&gt;</a><a href=\"http://translate.google.com/m.*\" class=\"s1\">(.+?)</a></div><br><div dir=\"ltr\" class=\"t0\">", source)[0]
			result = re.findall("=\"ltr\" class=\"t0\">(.+?)</div>", source)[0]
			Channel.send("%s: \002[%s to %s]\017 %s" % (line.split()[0][1:].split("!")[0], langtran[0], langtran[1], result))
		except:
			traceback.print_exc()