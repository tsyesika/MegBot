def main(connection, line):
	if len(line.split()) <= 3:
		connection.core["raw"].main(connection, "PART %s" % line.split()[2])
		return
	connection.core["raw"].main(connection, "PART %s" % line.split()[4])
	connection.core["privmsg"].main(connection, line.split()[2], "Parted.")