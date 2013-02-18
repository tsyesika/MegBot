import traceback
class Event():
	eventType = "Generic"

	def preInit(self, item, callback):
		pass

	def postInit(self, item, callback):
		pass

	def __init__(self, item, callback=None, eid=None):

		self.item = item
		self.callback = callback
		self.eid = eid
		
		self.postInit(item, callback)

	def event(self, event):
		if self.check(event):
			self.callback(event.item)

	def preCheck(self, event):
		pass

	def check(self, event):
		self.preCheck(event)

		self.cresult = event == self.item
		
		self.postCheck(event)
		return self.cresult

	def postCheck(self, event):
		pass

	def destoryable(self, eid):
		if eid == self.eid:
			return True
		return False

class IRCEvent(Event):
	eventType = "IRC"

	def check(self, event):
		for attr in dir(event.item):
			if attr.startswith("__"):
				continue
			try:
				remote = eval("event.item.%s" % attr)
				local = eval("self.item.%s" % attr)
				if remote and local:
					if not remote == local:
						return False 
			except:
				traceback.print_exc()
				return False
		return True


class Info():
    def __init__(self, line=None):
        if line == None:
            self.nick = ""
            self.action = ""
            self.raw = ""
            self.message = ""
            self.channel = ""
            self.plugin_name = ""
            self.trigger = ""
            self.args = []
            return

        line = line.split()

        # Lets pull things out.
        self.nick = line[0].split("!")[0][1:]
        self.action = line[1]
        self.raw = line
        self.message = "%s %s" % (line[3][1:], " ".join(line[4:]))
        self.channel = line[2]
        self.plugin_name = line[3][2:]
        self.trigger = line[3][1]
        self.args = line[4:]

class Handler():
	__events = {}

	def __init__(self):
		pass

	def register_event(self, event):
		""" registers an event """
		if not event.eventType in self.__events:
			self.__events[event.eventType] = set()
		self.__events[event.eventType].add(event)

	def unregister_event(self, eid):
		""" Takes all events which have the id (eid) """
		new = {}
		for s in self.__events:
			new[s] = set()
			for e in self.__events[s]:
				if not e.destoryable(eid):
					new[s].add(event)
		self.__events = new 

	def event(self, event):
		""" passes an event off to all registered events """
		if event.eventType in self.__events:
			for e in self.__events[event.eventType]:
				e.event(event)

def display(message):
	print "%s said %s in %s." % (message.nick, message.message, message.channel)

if __name__ == "__main__":
	# make events handler.
	eventHandler = Handler()

	# make an event to register
	info = Info()
	info.trigger = ","

	event = IRCEvent(info, display, "ILoveMoggersLotsAndLots72")
	eventHandler.register_event(event)

	# now take from stdin which will emulate new events
	# from IRC

	inp = raw_input("> ")
	while not inp.startswith("QUIT :"):
		if inp == "unregister":
			eventHandler.unregister_event("ILoveMoggersLotsAndLots72")
			inp = raw_input("> ")
			continue
		try:
			line = Info(inp)
			eventHandler.event(IRCEvent(line))
		except:
			print "Syntax error"
			traceback.print_exc()

		inp = raw_input("> ")