def main(connection, message, sock=None, end="\r\n"):
	""" Sends a PRIVMSG """
	if not sock:
		sock = connection.sock
	print "[OUT] %s" % message
	sock.sendall("%s%s" % (message, end))
	return
def initalise():
	""" Called when plugin is loaded """
	pass