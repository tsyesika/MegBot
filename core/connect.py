def main(connection):
	""" Sends a PRIVMSG """
	connection.sock.connect((connection.settings["address"], connection.settings["port"]))
	connection.core["raw"].main(connection, "NICK %s" % connection.settings["nick"])
	connection.core["raw"].main(connection, "USER 8 * %s :%s" % (connection.settings["ident"], connection.settings["realname"]))
	connection.running = True
	return
def initalise():
	""" Called on initalisation"""
	pass