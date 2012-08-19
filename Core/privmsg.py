def main(connection, channel, message):
	""" Sends a PRIVMSG """
	if type(message) != type(str):
		message = str(message)
	connection.core["Coreraw"].main(connection, "PRIVMSG %s :%s" % (channel, message))

def initalise():
	""" Called when plugin is loaded """
	pass
