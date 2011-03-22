import re, urllib2

def main(connection, line):
	if len(line.split()) <= 4:
		line = line + " " + line.split()[0].split("!")[0][1:]
	try:
		i = urllib2.urlopen("http://identi.ca/%s" % line.split()[-1])
		data = i.read()
		last = re.findall("<p class=\"entry-content\">(.+?)</p>", data)[0]
		name = re.findall("<title>(.+?) ", data)[0]
		time = re.findall(">about (.+?) ago</abbr>", data)[0]
		identification = re.findall("<li class=\"hentry notice\" id=\"notice-(.+?)\">", data)[0]
		
		#checks for url's
		last = re.sub("<span class=\"vcard\">.*?<span class=\"fn nickname\">(.+?)</span></a></span>", "\g<1>", last)
		last = re.sub("<a href=\"(.+?)\".*?>.*?<\/a>", "\g<1>", last)
		last = re.sub("<span class=\"(.+?)\".*?>.*?<\/span>", "", last)
		last = last.replace("&quot;", "\"")
		connection.core["privmsg"].main(connection, line.split()[2], "\002[%s]\017 %s - \002Aprox: %s\017 - http://www.identi.ca/notice/%s" % (name, last, time, identification))
	except:
		connection.core["privmsg"].main(connection, line.split()[2], "An error has occured")
		