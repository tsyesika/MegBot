import re, urllib2
def main(connection, line):
	if len(line.split()) <= 3:
		connection.core["privmsg"].main(connection, line.split()[2], "Please put a username")
	else:
		try:
			i = urllib2.urlopen("http://identi.ca/xray7224")
			data = i.read()
			last = re.findall("<p class=\"entry-content\">(.+?)</p>", data)[0]
			name = re.findall("<title>(.+?) ", data)[0]
			time = re.findall(">about (.+?) ago</abbr>", data)[0]
			connection.core["privmsg"].main(connection, line.split()[2], "\002[%s]\017 %s - \002Aprox: %s\017" % (name, last, time))
		except:
			connection.core["privmsg"].main(connection, line.split()[2], "An error has occured")
		