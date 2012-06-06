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

import socket, sys, traceback, os
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
		self.hooker = hooker
		if "Corelloader" in self.core.keys():
			self.libraries = self.core["Corelloader"].main(self)
		self.server = self.libraries["IRCObjects"].L_Server(self)
		self.server.__setuphooks__(self)
		self.plugins = {}
		self.sock = socket.socket()
		self.core["Coreconnect"].main(self)
		self.core["Corepluginloader"].main(self)
		#print self.core
		self.run()
	def run(self):
		while not self.running:
			sleep(.1)
		while True:
			data = self.core["Coreparser"].main(self, [])
			print data
			for line in data.split("\r\n"):
			 	if line:
					self.core["Coreping"].main(self, line.split())
					if len(line.split()) > 1:
						try:
							self.hooker.hook(self, line.split()[1], line)
						except:
							traceback.print_exc()
					if len(line.split()) > 3 and len(line.split()[3]) > 1 and line.split()[3][1] == self.settings["trigger"]:
						if line.split()[3][2:] in self.plugins.keys():
							try:
								self.core["Coreexecutor"].executor(self, line, line.split()[3][2:])
							except:
								traceback.print_exc() # Debug lines
								print self.times

if __name__ == "__main__":
	config = load_source("config", "config.py")
	coreplugins = {}
	for c in glob("Core/*.py"):
		# Thanks to webpigeon (https://github.com/xray7224/MegBot/issues/3)
		name = "Core%s" % os.path.splitext(os.path.basename(c))[0]
		coreplugins[name] = load_source(name, c)
	bots = {}
	for network in config.networks.keys():
		if not "active" in config.networks[network].keys() or config.networks[network]["active"]:
			bots[network] = start_new_thread(Bot, (config.networks[network], coreplugins["Corehooker"].Hooker(), coreplugins, config))
	try:
		while True:
			sleep(5)
	except KeyboardInterrupt:
		print "Ctrl-C been hit, run for your lives !"
		exit()
