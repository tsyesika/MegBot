def main(bot, message):
	if message.split()[0].split("!")[0][1:] == bot.settings["nick"]:
		# Bot quit.
		# initate reconnect.
		bot.running = False
