def main(connection, message=[]):
	""" Parses the text """
	message.append(connection.sock.recv(2048))
	if message[-1] == "":
		# Socket broken
		connection.running = False
		return ""
	if message[-1][-2:] == "\r\n":
		return "".join(message)
	return main(connection, message)
