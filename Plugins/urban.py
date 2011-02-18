import urllib2, re

def main(connection, line):
	if len(line.split()) <= 3:
		connection.core["privmsg"].main(connection, line.split()[2], "Please supply the word you want to be defined.")
		return
	google = urllib2.Request("http://www.urbandictionary.com/define.php?term=%s" % "+".join(line.split()[4:]))
	google.add_header("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3")
	google = urllib2.urlopen(google)
	source = google.read()
	try:
		definition = re.findall("<div class=\"definition\">(.+?)</div><div class=\"example\">(.+?)</div>", source)[0]
		definition = "%s: \002[%s]\017 - %s \002Example:\017 %s" % (line.split()[0][1:].split("!")[0], " ".join(line.split()[4:]), definition[0].replace("&quot", "\"").replace("<br/>",""), definition[1].replace("&quot;", "\"").replace("<br/>", ""))
	except:
		definition = "Sorry, can't find a definiton"
	connection.core["privmsg"].main(connection, line.split()[2], definition)

def initalisation(connection):
	pass