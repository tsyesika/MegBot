from imp import load_source
import os, traceback

class Hooker(object):
	"""Deals with the MegBot hooks system"""
	__hooks = {}

	def __init__(self):
		#register our own hooks (maybe there should be a user plugin?)
		self.register_hook('on_376', self.on_376)
		self.register_hook('on_353', self.on_353)
		self.register_hook('on_MODE', self.on_MODE)

	def hook(self, bot, act, line):
		"""Hooks plugins, etc..."""
		act = 'on_'+act
		if act not in self.__hooks.keys():
			return
		for callback in self.__hooks[act]:
			callback(bot, line)

	def register_hook(self, hook, callback):
		"""registers a new callback"""
		if hook not in self.__hooks.keys():
			self.__hooks[hook] = set()
		self.__hooks[hook].add(callback) 

	def unregister_hook(self, hook, callback):
		"""unregisters an existing callback"""
		if hook in self.__hooks.keys():
			self.__hooks[hook].remove(callback)

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
