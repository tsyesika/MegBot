import glob, imp, os

def main(connection, plugin=None):
	if plugin:
		if "unload" in dir(connection.plugins[plugin]):
			connection.plugins[plugin].unload(connection)
		connection.plugins[plugin] = imp.load_source(plugin, connection.config.paths["plugin"] + plugin + ".py")
		connnection.Server = connection.server
		if "init" in dir(connection.plugins[plugin]):
			connection.plugins[plugin].init(connection)
		
	else:
		for g in glob.glob(connection.config.paths["plugin"] + "*.py"):
			name = os.path.splitext(os.path.basename(g))[0]
			connection.plugins[name] = imp.load_source(name, g)
			connection.plugins[name].Server = connection.server
			connection.plugins[name].Helper = connection.libraries["IRCObjects"].L_Helper()
			connection.plugins[name].Web = connection.libraries["IRCObjects"].L_Web(connection)
			connection.plugins[name].Format = connection.libraries["IRCObjects"].L_Format
			if "init" in dir(connection.plugins[name]):
				connection.plugins[name].init(connection)
