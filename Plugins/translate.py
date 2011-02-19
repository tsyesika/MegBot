import urllib2, re, traceback

def main(connection, line):
	if len(line.split()) <= 3:
		connection.core["privmsg"].main(connection, line.split()[2], "Please supply lang|lang <text to translate> or languages")
		return
	if line.split()[4] == "languages":
		pass
	else:
		if line.split()[4].find("|")!=-1:
			#pipe used
			langpair = (line.split()[4].split("|")[0], line.split()[4].split("|")[1])
		else:
			langpair = ("auto", line.split()[4])
		try:
			google = urllib2.Request("http://translate.google.com/?text=%s&sl=%s&tl=%s" % ("+".join(line.split()[5:]), langpair[0], langpair[1]))
			google.add_header("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3")
			google = urllib2.urlopen(google)
			source = google.read()
			langtran = re.findall("<h3 id=headingtext class=\"\">(.+?) to (.+?) translation</h3>", source)[0]
			result = re.findall("onmouseout=\"this.style.backgroundColor='#fff'\">(.+?)</span></span></div></div><di", source)[0]
			connection.core["privmsg"].main(connection, line.split()[2], "%s: \002[%s to %s]\017 %s" % (line.split()[0][1:].split("!")[0], langtran[0], langtran[1], result))
		except:
			traceback.print_exc()

def initalisation(connection):
	pass