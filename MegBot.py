##
#This file is part of MegBot.
#
#   MegBot is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   MegBot is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with MegBot.  If not, see <http://www.gnu.org/licenses/>.
##

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
			data = self.core["parser"].main(self)
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
					if len(line.split()) > 3 and len(line.split()[3]) > 1 and line.split()[3][1] == self.settings["trigger"]:
						if line.split()[3][2:] in self.plugins.keys():
							try:
								self.core["executor"].executor(self, line, line.split()[3][2:])
							except:
								traceback.print_exc()

if __name__ == "__main__":
	config = load_source("config", "config.py")
	coreplugins = {}
	for c in glob("Core/*.py"):
		coreplugins[c.replace("Core/", "").replace(".py", "")] = load_source(c.replace("Core/", "").replace(".py", ""), c)
	bots = {}
	for network in config.networks.keys():
		if "active" in config.networks[network].keys() and config.networks[network]["active"]:
			bots[network] = start_new_thread(Bot, (config.networks[network], coreplugins["hooker"].Hooker(), coreplugins, config))
		elif not "active" in config.networks[network].keys():
			bots[network] = start_new_thread(Bot, (config.networks[network], coreplugins["hooker"].Hooker(), coreplugins, config))
	try:
		while True:
			sleep(5)
	except KeyboardInterrupt:
		print "Ctrl-C been hit, run for your lives !"
		exit()