import socket, traceback, glob

from sys import exit
from time import sleep, ctime
from multiprocessing import Process
from imp import load_source

class Bot(object):
	def __init__(self, settings, hooker, plugins, config, core):
		"""Initalises bot"""
		self.core = core
		self.config = config
		self.settings = settings
		self.running = False
		self.channels = {}
		self.plugins = plugins
		self.hooker = hooker
		if self.settings["ipv6"]:
			self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		else:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if self.settings["ssl"]:
			import ssl
			self.sock = ssl.wrap_socket(self.sock)
		self.core["connect"].main(self)
		self.runner()
	def die(self):
		"""Stops bot from running"""
		self.raw("QUIT :Ctrl-C at shell")
		self.sock.close()
	def runner(self):
		"""Does the shizzle for the shizzle bizzle to dizzle *"""
		self.running = True
		while self.running:
			data = self.sock.recv(2048)
			for line in data.split("\r\n"):
				if line:
					print "[IN] %s" % line
					if line.split()[0] == "PING":
						self.raw("PONG %s" % line.split()[1])
					elif 1 < len(line.split()):
						if ("on_%s" % line.split()[1]) in dir(self.hooker):
							eval("self.hooker.on_%s(self, line)" % line.split()[1])
						if line.split()[1] == "PRIVMSG":
							#check if plugin needs to be called
							try:
								print line.split()
								if line.split()[3][1] == config.trigger:
									print 1
									if line.split()[3][2:] in self.plugins.plugins.keys():
										print 2
										self.plugins.plugins[line.split()[3][2:]].main(self, line.split())
							except:
								traceback.print_exc()
				

class Plugins(object):
	def __init__(self):
		self.plugin_path = config.paths["plugin"]
		self.plugins = {}
	def load(self, bot, plugin):
		"""Loads plugin"""
		if self.exists(plugin):
			if plugin in self.plugins.keys():
				return False
			else:
				self.plugins[plugin] = load_source(plugin, self.find_path(plugin))
			return True
		else:
			return False
	def find_path(self, plugin):
		"""Returns path of plugin"""
		return "%s/%s.py" % (self.plugin_path, plugin)
	def exists(self, plugin):
		"""Checks if a plugin exists"""
		plugins = self.list_plugins()
		if plugin in plugins:
			return True
		return False
	def list_plugins(self):
		return [p.split("/")[-1].replace(".py", "") for p in glob.glob(self.plugin_path + "/*.py")]
	def autoload(self, bot=None):
		"""Finds all plugins and loads them"""
		for plugin in self.list_plugins():
			self.load(bot, plugin)
		

if __name__ == "__main__":
	config = load_source("config", "config.py")
	coremodules = {}
	for module in glob.glob("core/*.py"):
		coremodules[module.replace("core/", "").replace(".py", "")] = load_source(module.replace("core/", "").replace(".py", ""), module)
		coremodules[module.replace("core/", "").replace(".py", "")].config = config
		coremodules[module.replace("core/", "").replace(".py", "")].initalise()
	bots = {}
	plug = Plugins()
	plug.autoload()
	for network in config.networks.keys():
		bots[network] = Process(target=Bot, args=(config.networks[network], coremodules["hooker"].Hooker(), plug, config, coremodules))
		bots[network].start()
	try:
		while True:
			sleep(5)
	except KeyboardInterrupt:
		print "Ctrl-C been hit, run for your lives !"
		for b in bots.keys():
			if bots[b].is_alive():
				bots[b].stop()
				bots[b].terminate()
		exit()