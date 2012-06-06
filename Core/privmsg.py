def main(connection, channel, message):
	""" Sends a PRIVMSG """
	connection.core["Coreraw"].main(connection, "PRIVMSG %s :%s" % (channel, message))

def initalise():
	""" Called when plugin is loaded """
	pass
