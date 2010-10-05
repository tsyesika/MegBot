import socket, config, imp, glob, os, thread, ssl, time, traceback, sys

def restart(name):
	"""Restarts a bot instance"""
	if name in connections.keys():
		del connections[name]
		connections[name] = Bot(config.connections[name], name)
		thread.start_new_thread(connections[name].connect, ())
		thread.start_new_thread(connections[name].fireup, ())
	for bot in connections.keys():
		connections[bot].other_networks = connections
	print "---> Relinked bots"
class Bot():
	def __init__(self, settings, name):
		self.other_networks = None #Holder, filled when all instances created.
		self.connected = False
		self.name = name
		self.settings = settings
		self.plugins = {}
		self.previous_messages = []
		if settings["ipv6"]:
			if config.debug_mode:
				print "[DEBUG] IPV6 on %s" % settings["name"]
			self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		else:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if settings["ssl"]:
			if config.debug_mode:
				print "[DEBUG] IPV4 on %s" % settings["name"]
			self.sock = ssl.wrap_socket(self.sock)
	def raw(self, message, headers=True):
		"""Sends a raw irc message"""
		ready = ""
		if headers:
			ready = "%s\r\n" % message
		else:
			ready = message
		self.sock.sendall(message)
	def privmsg(self, person, message):
		"""privmesgs a person/channel"""
		self.raw("PRIVMSG %s :%s" % (person, message))
	def find_info(self, line):
		"""Gets info from raw string"""
		info = {}
		try:info["raw"] = line
		except:info["raw"] = "Unknown"
		try:info["nick"] = line.split()[0].split("!")[0][1:]
		except:info["nick"] = "Unknown"
		try:info["host"] = line.split()[0].split("!")[1]
		except:info["host"] = "Unknown"
		try:info["vhost"] = line.split()[0].split("@")[1]
		except:info["vhost"] = "Unknown"
		try:info["mode"] = line.split()[1]
		except:info["mode"] = "Unknown"
		try:info["cmd"] = line.split()[3][2:]
		except:info["cmd"] = "Unknown"
		try:info["trig"] = line.split()[3][1]
		except:info["trig"] = "Unknown"
		info["args"] = []
		if 4 <= len(line.split()):
			for arg in line.split()[4:]:
				info["args"].append(arg)
		return info
	def on_call(self, call, line):
		"""First line hook management"""
		info = self.find_info(line)
		if "on_" + call in dir(self):
			#Is in core
			exec("self.on_%s(%s, %s)" % (call, self, info))
		for plugin in self.plugins.keys():
			if "on_%s" % call in self.plugins[plugin].keys:
				exec("self.plugins[plugin].on_%s(%s, %s)" % (call, self, info))
	def connect(self):
		"""Connects to network"""
		if config.debug_mode:
			print "[DEBUG] %s:%s (%s, %s)" % (self.settings["address"], self.settings["port"], type(self.settings["address"]), type(self.settings["port"]))
		self.sock.connect((self.settings["address"], self.settings["port"]))
		print "---> Connecting to %s" % self.settings["name"]
		print "NICK %s" % self.settings["nick"]
		print "USER 8 * %s :%s" % (self.settings["ident"], self.settings["realname"])
		self.raw("NICK %s" % self.settings["nick"])
		self.raw("USER 8 * %s :%s" % (self.settings["ident"], self.settings["realname"]))
		self.connected = True
	def fireup(self):
		while not self.connected:
			pass
		while True:
			data = self.sock.recv(2048)
			for line in data.split("\r\n"):
				if line:
					print line
					self.previous_messages.append(line)
					self.on_call("DRECV", line)
					if line.split()[0][1:] == "PING":
						self.raw("PONG %s" % line.split()[1:], False)
						self.on_call("PING", line)
					elif line.lower().startswith("error :closing link"):
						if config.debug_mode:
							print "[DEBUG] disconnected from network."
						print "---> Restarting"
						self.sock.close()
						restart(self.name)
					elif len(line.split()) != 1:
						self.on_call(line.split()[1], line)
						if line.split()[1] == "PRIVMSG":
							#If a privmsg has been recived
							info = self.find_info()
							if info["cmd"] == "VERSION\x01":
								#CTCP version 
								self.on_call("VERSION")
								self.notice(self.info["nick"], "\x01MegBot 0.06 Developer Preview (unstable)\x01")
							elif info["cmd"] == "TIME\x01":
								self.notice(self.info["nick"], "\x01%s\x01" % time.strftime("%A %d %b %Y, %H:%M:%S %Z"))
								self.on_call("TIME")
							elif info["cmd"] == "CLIENTINFO":
								self.notice(self.info["nick"], "\x01MegBot 0.06 Developer Preview (unstable)\x01")
							elif info["cmd"] == "PING\x01":
								self.notice(self.info["nick"], "\x01%s\x01" % ())
							elif info["cmd"] == "SOURCE\x01":
								self.notice(self.info["nick"], "\x01http://megworld.co.uk/\x01")
								self.on_call("SOURCE")
							elif info["trig"] == self.settings["trigger"] and info["cmd"] in self.plugins.keys():
								try:
									self.plugins[info["cmd"]].main(self, info)
								except:
									if config.debug_mode:
										print "[DEBUG] with plugin %s" % (info["cmd"])
										traceback.print_exc()
	def on_376(self, info):
		"""Applies modes & execute commands on connect & joins channels"""
		if self.settings["modes"]:
			mode_msg = ""
			for mode in self.settings["modes"]:
				mode_msg = mode_msg + mode[0]
			mode_msg = mode_msg + " "
			for mode in self.settings["modes"]:
				mode_msg = mode_msg + mode[1:]
			self.raw("MODE %s %s" % (self.settings["nick"], mode_msg))
		if self.settings["commands-execute"]:
			for command in self.settings["commands-execute"]:
				self.raw(command)
		if self.settings["name"] in config.channels.keys():
			join_msg = ""
			passwds = []
			for channel in config.channels[self.settings["name"]].keys():
				if config.channels[self.settings["name"]][channel]["password"]:
					join_msg = join_msg + channel + ","
					passwds.append(config.channels[self.settings["name"]][channel]["password"])
			if join_msg:
				for channels in config.channels[self.settings["name"]].keys():
					join_msg = join_msg + channel + ","
				join_msg = join_msg[:-1] + ",".join(passwds)
			else:
				join_msg = ",".join(config.channels[self.settings["name"]].keys())
			self.raw("JOIN %s" % join_msg)
		
			
if "__main__" == __name__:
	connections = {}
	for connection in config.connections.keys():
		connections[connection] = Bot(config.connections[connection], connection)
		while not connections[connection].connected:
			connections[connection].connect()
		print "---> Creating %s bot..." % connection
	if connections != 1:
		for connection in connections.keys():
			connections[connection].other_networks = connections
		print "---> bots linked"
	print "---> Cleaning plugins"
	for plugin in glob.glob(config.plugin_dir + "/*.pyc"):
		if os.path.isfile(plugin[:-1]):
			os.remove(plugin)
			if config.debug_mode:
				print "[DEBUG] %s cleaned" % plugin
		else:
			if config.debug_mode:
				print "[DEBUG] %s no source for %s" % plugin
	print "---> Loading plugins"
	for connection in connections.keys():
		for plugin in glob.glob(config.plugin_dir + "/*.py*"):
			connections[connection].plugins[plugin] = imp.load_source(plugin.replace(".py", "").replace(".pyc", "").replace(config.plugin_dir + "/", ""), plugin)
		thread.start_new_thread(connections[connection].fireup, ())
	print "---> Inital bot online"
	try:
		while True:
			pass
	except KeyboardInterrupt:
		print "\n---> Sending Exit to bots"
		for connection in connections.keys():
			connections[connection].raw("QUIT :Ctrl-C at shell")
			connections[connection].sock.close()
		print "---> Delinking bots"
		for connection in connections.keys():
			del connections[connection]
		print "---> Exiting"
		sys.exit()
	finally:
		pass
	
		