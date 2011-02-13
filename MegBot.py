import socket, traceback, sys

from thread import start_new_thread
from sys import exit
from time import sleep, ctime
from imp import load_source
from glob import glob

class Bot(object):
	def __init__(self, settings, hooker, plugins):
		"""Initalises bot"""
		self.settings = settings
		self.running = False
		self.core = plugins
		self.sock = socket.socket()
		coreplugins["connect"].main(self)
		self.run()
	def run(self):
		while not self.running:
			sleep(.5)
		#sleep(2)
		while True:
			data = self.sock.recv(2048)
			print data

if __name__ == "__main__":
	config = load_source("config", "config.py")
	coreplugins = {}
	for c in glob("core/*.py"):
		coreplugins[c.replace("core/", "").replace(".py", "")] = load_source(c.replace("core/", "").replace(".py", ""), c)
	bots = {}
	for network in config.networks.keys():
		bots[network] = start_new_thread(Bot, (config.networks[network], coreplugins["hooker"].Hooker(), coreplugins))
	try:
		while True:
			sleep(5)
	except KeyboardInterrupt:
		print "Ctrl-C been hit, run for your lives !"
		exit()