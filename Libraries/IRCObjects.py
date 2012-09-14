# -*- coding: utf-8 -*-
##
# IRC Objects
##

#import re, time
import time, re, platform, os
from Data.HTMLEnterties import *

class Standard():
	""" Never instantiate """
	def __setuphooks__(self, connection):
		if "Corehooker" in connection.core.keys():
			# Woot, we got ability to have hooks
			for anm in dir(self):
				if anm.startswith("on_"):
					connection.hooker.register_hook(anm, eval("self.%s" % anm))
					
class Info(Standard):
	def __init__(self, line):
		if line == None:
			self.nick, self.action. self.raw, self.channel, self.plugin_name, self.trigger, self.args = "", "", "", "", "", []
			return
		self.nick = line.split()[0].split("!")[0][1:]
		self.action = line.split()[1]
		self.raw = line
		self.message = "%s %s" % (line.split()[3][1:], " ".join(line.split()[4:]))
		self.channel = line.split()[2]
		self.plugin_name = line.split()[3][2:]
		self.trigger = line.split()[3][1]
		self.args = line.split()[4:]

class L_Helper(Standard):
	def StripHTML(self, message):
		p = re.compile(r'<.*?>')
		return p.sub("", message)
	def ConvertHTMLReversed(self, message):
		"""
		Converts some HTML reversed (&quot; &apos; etc...)
		message = The message you'd like to convert.
		Returns unicode string (even if message was str)
		(http://www.w3schools.com/tags/ref_entities.asp)
		"""
		
		# convert it to unicode
		message = message.decode("utf-8")
		for item in HTML_Enterties.keys():
			message = message.replace(item, HTML_Enterties[item])
		return message
		
	def TimeZoneCorrect(self, t, pre_timezone, post_timezone):
		"""
		This will convert from one timezone to another.
		t = time.time() - seconds after the EPOC
		pre_timezone = timezone t is - +/-XXXX producable by time.strftime("%z")
		post_timezone = timezone t should be in - UTC", "BST", etc.. producable by time.strftime("%Z")
		"""
		utc = time.strptime(time.strftime("%b %d %H:%M:%S %Y ", time.gmtime(t))+pre_timezone, "%b %d %H:%M:%S %Y %Z")
		# convert to post_timezone
		et = time.strptime(time.strftime("%b %d %H:%M:%S %Y ", utc)+post_timezone, "%b %d %H:%M:%S %Y %Z")
		return ime.mktime(et)
		
	def HumanTime(self, t=time.time(), parse=None, f=None):
		"""
		This function will return a string which will give a useful
		offset for humans ("5 minutes ago", "6 months ago", etc...):
		
		t = time (float or string) froom time.time() or formatted (required)
		parse = a string for formatting e.g. "%a %b %d %H:%M%S %Y %Z" (required if t is a str) 
		f = from an offset, defaults to time.time() (now), must be a float.
		"""
		if type(t) == type("") and parse:
			t = time.strptime(t, parse)
			t = time.mktime(t)
		else:
			t = float(t)
		# Find out time passed from now/f.
		if f:
			t = f-t
		else:
			t = time.time()-t
		print t
		# Work out time passed.
		if t < 60:
			return "Less than a minute"
		elif (t / 60) <= 60:
			# a hour
			m = int(t/60.0 + .5) # .5 to avoid floor rounding.
			if m <= 1:
				return "A minute"
			else:
				return "%s minutes" % m
		elif ((t / 60) / 60) <= 24:
			# a day
			h = int(t / 60.0 / 60.0 + 0.5)
			if h <= 1:
				return "A hour"
			else:
				return "%s hours" % h
		elif (((t / 60) / 60) / 24) <= 7:
			# a week
			d = int(t / 60.0 / 60.0 / 24.0 + 0.5)
			if d <= 1:
				return "A day"
			else:
				return "%s days" % d
		elif ((((t / 60) / 60) / 24) / 7) <= 4:
			# a month (29 days, lowest except 28)
			w = int(t / 60.0 / 60.0 / 24.0 / 7.0 + 0.5)
			if w <= 1:
				return "A week"
			else:
				return "%s weeks" % w
		elif (((t / 60) / 60) / 24) <= 365 :
			# a year (below a decade)
			y = int(t / 60.0 / 60.0 / 24.0 / 365.0 + 0.5)
			if y <= 1:
				return "A year"
			else:
				return "%s years" % y
		elif ((((t / 60) / 60) / 24) / 365) <= 10:
			# a decade (decade - century)
			d = int(t / 60.0 / 60.0 / 24.0 / 365.0 / 10.0 + 0.5)
			if d <= 1:
				return "A decade"
			else:
				return "%s decades" % d
		else:
			c = int(t / 60.0 / 60.0 / 24.0 / 365.0 / 100.0 + 0.5)
			if c <= 1:
				return "A century"
			else:
				return "%s centuries" % c
		

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
