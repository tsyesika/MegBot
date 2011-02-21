from imp import load_source
import os, traceback

class Hooker(object):
	def hook(self, bot, act, line):
		"""Hooks plugins, etc..."""
		if ("on_%s" % act) in dir(self):
			eval("self.on_%s(bot, line)" % act)
		for plugin in bot.plugins.keys():
			if ("on_%s" % act) in dir(bot.plugins[plugin]):
				eval("bot.plugins[plugin].on_%s(bot, line)" % act)
	def on_376(self, bot, message):
		"""End of MOTD"""
		for channel in bot.settings["channels"]:
			bot.core["join"].main(bot, channel)
		if bot.settings["NSPassword"]:
			bot.core["privmsg"].main(bot, "NickServ", "identify %s" % bot.settings["NSPassword"])
		for cmd in bot.settings["commands"]:
			bot.core["raw"].main(bot, cmd)
	def on_353(self, bot, message):
		"""Names on joining of a channel"""
		channel = message.split("#")[1].split()[0]
		nicks = message.split(":")[2].split()
		bot.channels[channel] = {"all":[], "hop":[], "sop":[], "aop":[], "vop":[], "non":[], "founder":[]}
		for nick in nicks:
			if nick[0] in ["+", "&", "@", "%", "~"]:
				bot.channels[channel][bot.config.permissions[nick[0]]].append(nick[1:])
				bot.channels[channel]["all"].append(nick[1:])
			else:
				bot.channels[channel]["non"].append(nick)
				bot.channels[channel]["all"].append(nick)
	def on_MODE(self, bot, message):
		"""When a mode is set"""
		try:
			mode = message.split()[3][1:]
			channel = message.split()[2][1:]
			for v1, m in enumerate(mode):
				if m in ["a", "o", "q", "h", "v"]:
					if len(line.split()) <= 3:
						nick = line.split()[0][1:].split("!")[0]
					else:
						nick = message.split()[4:][v1]
					if m == "a":
						bot.channels[channel]["sop"].append(nick)
					elif m == "o":
						bot.channels[channel]["aop"].append(nick)
					elif m == "h":
						bot.channels[channel]["hop"].append(nick)
					elif m == "v":
						bot.channels[channel]["vop"].append(nick)
					elif m == "q":
						bot.channel[channel]["founder"].append(nick)
		except:
			traceback.print_exc()
def initalise():
	""" Called when plugin is loaded """
	pass
def main():
	""" Holder """
	pass