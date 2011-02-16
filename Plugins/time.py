import re, urllib2

def main(connection, line):
	if len(line.split()) <= 3:
		connection.core["privmsg"].main(connection, line.split()[2], "Please enter a location")
		return
	google = urllib2.Request("http://www.google.com/search?q=time+%s" % line.split()[4].replace(" ", "%20"))
	google.add_header("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3")
	google = urllib2.urlopen(google)
	source = google.read()
	try:
		time = re.findall("><tr><td style=\"font-size:medium\"><b>(.+?)</b>", source)[0]
		connection.core["privmsg"].main(connection, line.split()[2], "Time: %s" % time)
	except:
		connection.core["privmsg"].main(connection, line.split()[2], "Sorry, couldn't retrive time.")
		
def initalisation(connection):
	pass