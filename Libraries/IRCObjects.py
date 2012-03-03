# -*- coding: utf-8 -*-
##
# IRC Objects
##
class Standard():
	""" Never instantiate """
	def __setuphooks__(self, connection):
		if "hooker" in connection.core.keys():
			# Woot, we got ability to have hooks
			for anm in dir(self):
				if anm.startswith("on_"):
					connection.hooker.register_hook(anm, eval("self.%s" % anm))
class L_Channel(Standard):
	def __init__(self, connection, name):
		self.connection = connection # Connection of bot, instance.
		self.name = name
		self.topic = ""
		self.modes = []
		self.voiced = []
		self.ops = []
		self.halfops = []
		self.normals = []
		self.nicks = []
		for person in self.nicks:
			if person[0] in ["&", "~", "@"]:
				self.ops.append(erson[1:])
			elif person[0] == "%":
				self.halfops.append(person[1:])
			elif person[0] == "+":
				self.voiced.append(person[1:])
			else:
				self.users.append(person[1:])
		self.cleaned_nicks = self.ops + self.halfops + self.normals #All nicks but without any modes
		self.recently_sent = []
		self.recently_recved = []
	def send(self, message):
		self.connection.core["privmsg"].main(self.connection, self.name, message)
		self.recently_sent.append(message)
		if len(self.recently_sent) <= 5:
			self.recently_sent.pop(0)
	def on_JOIN(self, connection, message):
		nick = message.split()[0][1:].split("!")[0]
		self.nicks.append(nick)
		self.normals.append(nick)
	def on_MODE(self, connection, message):
		mode = message.split()[3]
		if len(message.split()) > 4:
			nick = message.split()[4]
			def a(x, y):
				if x in self.normals:
					self.normals.remove(x)
				y.append(x)
			def r(x, y):
				y.remove(x)
				if not (x in self.voiced or x in self.ops or self.halfops):
					self.normals.append(x)
			if mode[0] == "-":
				func = r
			elif mode[1] == "+":
				func = a
			else:
				return
			# Now to check which mode...
			mode = mode[1:]
			for m in range(len(mode)):
				cm = mode[m] # current mode
				if cm.lower() == "o":
					func(nick, self.ops)
				elif cm.lower() == "h":
					func(nick, self.halfops)
				elif cm.lower() == "v":
					func(nick, self.voiced)
		else:
			def r(x):
				if x in self.modes:
					self.modes.remove(x)
			def a(x):
				if not x in self.modes:
					self.modes.append(x)
			if mode[0] == "+":
				func = a
			elif mode [0] == "-":
				func = r
			else:
				return
			# Now check which mode...
			mode = mode[1:]
			for m in range(len(mode)):
				cm = mode[m]
				func(m)
	def on_TOPIC(self, connection, message):
		new_topic = " ".join(message.split()[4:])[1:]
		self.topic = new_topic
	def on_PRIVMSG(self, connection, message):
		self.recently_recved.append(" ".join(message.split()[4:]))
		if len(self.recently_recved) > 5:
			self.recently_recved.pop(0)
	def on_353(self, connection, message):
		message = message.split()
		message = message[message.index(self.name)+1:]
		message[0] = message[0][1:] # ":" is put on the front of this.
		for n in message:
			self.nicks.append(n)
			if n[0] in ["&", "@", "~"]:
				self.ops.append(n[1:])
			elif n[0] == "%":
				self.halfops.append(n[1:])
			elif n[0] == "+":
				self.voiced.append(n[1:])
			else:
				self.normals.append(n)
	def on_332(self, connection, message):
		message = message.split()
		message = " ".join(message[message.index(self.name)+1:])[1:]
		self.topic = message
		
		

	