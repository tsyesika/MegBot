def main(connection):
	""" Connects to irc (by setting up socket and passing info to ircd) """
	if connection.settings["ssl"]:
		import ssl # Moved here as ssl is excluded on some python installs distributed with some linuxs 
		connection.sock = ssl.wrap_socket(connection.sock)
	connection.sock.connect((connection.settings["address"], connection.settings["port"]))
	connection.core["raw"].main(connection, "NICK %s" % connection.settings["nick"])
	connection.core["raw"].main(connection, "USER 8 * %s :%s" % (connection.settings["ident"], connection.settings["realname"]))
	connection.running = True
	return
def initalise():
	""" Called on initalisation"""
	pass
