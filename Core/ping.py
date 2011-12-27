def main(bot, message):
	"""Handles the PINGS"""
	if message[0] == "PING":
		bot.core["raw"].main(bot, "PONG %s" % message[1])
