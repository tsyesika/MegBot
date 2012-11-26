def main(connection, channel, message):
	""" Sends a PRIVMSG """
	if len(message) > 400:
		to_send = []
		for x in range((len(message) % 400) + 1):
			connection.core["Coreraw"].main(connection, "PRIVMSG %s :%s" % (channel, message[x*400:x*400*2]))
		
	if type(message) != type(str):
		message = str(message)
	connection.core["Coreraw"].main(connection, "PRIVMSG %s :%s" % (channel, message))

def initalise():
	""" Called when plugin is loaded """
	pass
