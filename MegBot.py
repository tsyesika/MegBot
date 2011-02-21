import socket, sys, traceback

from thread import start_new_thread
from sys import exit
from time import sleep, ctime
from imp import load_source
from glob import glob

class Bot(object):
	def __init__(self, settings, hooker, plugins, config):
		"""Initalises bot"""
		self.config = config
		self.settings = settings
		self.running = False
		self.channels = {}
		self.core = plugins
		self.plugins = {}
		self.hooker = hooker
		self.sock = socket.socket()
		self.core["connect"].main(self)
		self.core["pluginloader"].main(self)
		self.run()
	def run(self):
		while not self.running:
			sleep(.5)
		while True:
			data = self.sock.recv(2048)
			for line in data.split("\r\n"):
			 	if line:
					print "[IN] %s" % line.split()
					if line.split()[0] == "PING":
						self.core["raw"].main(self, "PONG %s" % line.split()[1])	
					if len(line.split()) > 1:
						try:
							self.hooker.hook(self, line.split()[1], line)
						except:
							traceback.print_exc()
					if len(line.split()) > 3 and len(line.split()[3]) > 1 and line.split()[3][1] == self.config.trigger:
						if line.split()[3][2:] in self.plugins.keys():
							try:
								self.plugins[line.split()[3][2:]].main(self, line)
							except:
								traceback.print_exc()

if __name__ == "__main__":
	config = load_source("config", "config.py")
	coreplugins = {}
	for c in glob("core/*.py"):
		coreplugins[c.replace("core/", "").replace(".py", "")] = load_source(c.replace("core/", "").replace(".py", ""), c)
	bots = {}
	for network in config.networks.keys():
		bots[network] = start_new_thread(Bot, (config.networks[network], coreplugins["hooker"].Hooker(), coreplugins, config))
	try:
		while True:
			sleep(5)
	except KeyboardInterrupt:
		print "Ctrl-C been hit, run for your lives !"
		exit()