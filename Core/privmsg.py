def main(connection, channel, message, recurse=False):
	""" Sends a PRIVMSG """
	# Todo, stop it chopping words up.
	
	pre_message = "PRIVMSG %s :" % (channel)

	# Max length of message can be 510 (512 inc. \r\n so 510 as raw adds those).
	MAX_LENGTH = 510 - len(pre_message)
	messages = [message[i:i+MAX_LENGTH] for i in range(0, len(message), MAX_LENGTH)]
	
	# now send to raw.
	for message in messages:
		connection.core["Coreraw"].main(connection, "%s%s" % (pre_message, message))
