def main(connection, line):
	if len(line.split()) <= 3:
		connection.core["privmsg"].main(connection, line.split()[2], "Please specify a channel to join.")
		return
	connection.core["raw"].main(connection, "JOIN %s" % line.split()[4])
	connection.core["privmsg"].main(connection, line.split()[2], "Joined.")