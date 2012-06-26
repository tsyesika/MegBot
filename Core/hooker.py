from imp import load_source
import os, traceback

class Hooker(object):
	"""Deals with the MegBot hooks system"""
	__hooks = {}

	def __init__(self):
		self.register_hook('on_376', load_source("on_376", "Core/on_376.py").main)
		self.register_hook('on_353', load_source("on_353", "Core/on_353.py").main)
		self.register_hook('on_MODE', load_source("on_MODE", "Core/on_MODE.py").main)
		self.register_hook('on_422', load_source("on_376", "Core/on_376.py").main)
		self.register_hook('on_QUIT', load_source("on_QUIT", "Core/on_QUIT.py").main)
	def hook(self, bot, act, line):
		"""Hooks plugins, etc..."""
		act = 'on_'+act
		if act not in self.__hooks.keys():
			return
		for callback in self.__hooks[act]:
			if line.split()[0] == "#":
				callback.Channel = bot.channels[line.split()[1]]
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
def main():
	""" Holder """
	pass
