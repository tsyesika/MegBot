import imp, os, urllib2, shutil

def main(connection, line):
	if len(line.split()) <= 3:
		connection.core["privmsg"].main(connection, line.split()[2], "Please enter plugin name.")
		return
	if line.split()[4].find("/")!=-1:
		try:
			pluginname = line.split()[4].split("/")[-1]
			if not pluginname.endswith(".py"):
				pluginname = pluginname + ".py"
			newplugin = open("temp", "w")
			plugin = urllib2.urlopen(line.split()[4])
			newplugin.write(plugin.read())
			newplugin.close()
			shutil.move("temp", connection.config.paths["plugin"] + pluginname)
			connection.plugins[pluginname.replace(".py", "")] = imp.load_source(pluginname.replace(".py", ""), connection.config.paths["plugin"] + pluginname)
			connection.core["privmsg"].main(connection, line.split()[2], "Plugin has been retrived & loaded.")
			print connection.plugins
			return
		except:
			connection.core["privmsg"].main(connection, line.split()[2], "Failed to retrive plugin or load.")
	if os.path.isfile(connection.config.paths["plugin"] + line.split()[4] + ".py"):
		connection.plugins[line.split()[4]] = imp.load_source(line.split()[4], connection.config.paths["plugin"] + cyline.split()[4] + ".py")
	else:
		connection.core["privmsg"].main(connection, line.split()[2], "Can't find plugin.")
		return
	if line.split()[4] in connection.plugins.keys():
		connection.core["privmsg"].main(connection, line.split()[2], "Plugin has been reloaded.")
	else:
		connection.core["privmsg"].main(connection, line.split()[2], "Plugin has been loaded.")
		
def initalisation(connection):
	pass