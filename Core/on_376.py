def main(bot, message):
	"""End of MOTD"""
	for channel in bot.settings["channels"]:
		bot.core["join"].main(bot, channel)
	if bot.settings["NSPassword"]:
		bot.core["privmsg"].main(bot, "NickServ", "identify %s" % bot.settings["NSPassword"])
	for cmd in bot.settings["commands"]:
		bot.core["raw"].main(bot, cmd)