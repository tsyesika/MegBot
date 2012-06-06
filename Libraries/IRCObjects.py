# -*- coding: utf-8 -*-
##
# IRC Objects
##
class Standard():
	""" Never instantiate """
	def __setuphooks__(self, connection):
		if "Corehooker" in connection.core.keys():
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
		self.connection.core["Coreprivmsg"].main(self.connection, self.name, message)
		self.recently_sent.append(message)
		if len(self.recently_sent) <= 5:
			self.recently_sent.pop(0)
	def on_JOIN(self, connection, message):
		nick = message.split()[0][1:].split("!")[0]
		self.nicks.append(nick)
		self.normals.append(nick)
	def set_topic(self, topic):
		self.topic = topic
		self.connection.server.raw("TOPIC %s :%s" % (self.name, topic))
	def voice(self, nick):
		if self.connection.server:
			self.connection.server.raw("MODE %s +v %s" % (self.name, nick))
	def devoice(self, nick):
		if self.connection.server:
			self.connection.server.raw("MODE %s -v %s" % (self.name, nick))
	def op(self, nick):
		if self.connection.server:
			self.connection.server.raw("MODE %s +o %s" % (self.name, nick))
	def deop(self, nick):
		if self.connection.server:
			self.connection.server.raw("MODE %s -o %s" % (self.name, nick))
	def set_mode(self, mode):
		if self.connection.server:
			self.connection.server.raw("MODE %s %s" % (self.name, mode))
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
		
class L_Server(Standard):
	def __init__(self, connection):
		self.connection = connection
		self.channels = self.connection.channels
		self.users = 0
		self.servers = 0
		self.channels = 0
		self.ops = 0
		self.motd = []
		self.nick = connection.settings["nick"]
	def on_JOIN(self, connection, message):
		self.channels = self.connection.channels
	def send(self, nick, message=None):
		if not message:
			# Assumes it's a raw message
			self.connection.core["Coreraw"].main(connection, nick)
		else:
			self.connecton.core["Coreprivmsg"].main(conneciton, nick, message)
	def join(self, channel):
		self.connection.core["Corejoin"].main(connection, channel)
	def part(self, channel):
		self.connection.core["Corepart"].main(connection, channel)
	def on_266(self, connection, message):
		number = message.split()[-3]
		try:
			self.users = int(number)
		except:
			pass
	def on_251(self, connection, message):
		number = message.split()[-2]
		try:
			self.servers = int(number)
		except:
			pass
	def on_254(self, connection, message):
		number = message.split()[-3]
		try:
			self.channels = int(number)
		except:
			pass
	def on_252(self, connection, message):
		number = message.split()[-3]
		try:
			self.ops = int(number)
		except:
			pass
	def on_372(self, connection, message):
		self.motd.append(" ".join(message.split()[4:]))
		if self.motd[-1][-2:] == "\r\n":
			self.motd[-1] = self.motd[:-2]
	def nick(self, nick):
		# sets nickname
		self.connection.core["Coreraw"].main(connection, "NICK %s" % nick)
		self.connection.hooker.hook(self, "nick", nick)
	def on_NICK(self, connection, nick):
		self.nick = nick
	def mode(self, user, mode=None):
		if not mode:
			# Assumes user to be mode and it to be set on self
			mode = user
			user = self.nick
		self.raw("MODE %s %s" % (user, mode))
	def oper(self, user, password):
		self.raw("OPER %s %s" % (user, password))
