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

import imp, os, urllib2, shutil,time

def FindName(args):
	"""
	Returns first argument in args which doesn't start with -
	"""
	if not args:
		return
	if args[0][0] != "-":
		return args[0]
	return FindName(args[1:])
	
def main(connection, line):
	"""
	Handles plugin reloading for Core, Libraries, Config and normal user plugins.
	This will handle flags within the IRC. If also the libraries are being reloaded the
	special case of Helper, Web and Server are re-seeded in all the plugins the bot has.
	
	Once an auth system is inplace the http:// loading needs adding & pastebin loading.
	"""
	if not Info.args:
		Channel.send("You must give a plugin name")
		return
	# Lets look for flags
	# -c = core
	# -l = library
	# -C = config
	if "-c" in Info.args:
		# Okay - core plugins
		name = "Core/%s.py" % FindName(Info.args)
	elif "-l" in Info.args:
		# okay - libraries
		name = "Libraries/%s.py" % FindName(Info.args)
	elif "-C" in Info.args:
		# okay - config
		name = "config.py"
	elif FindName(Info.args):
		# Must be a normal plugin
		name = "Plugins/%s.py" % FindName(Info.args)
	else:
		Channel.send("You need to enter a plugin to reload/load")
		return
	
	print "Debug: %s" %  name
	if not os.path.isfile(name):
		Channel.send("Can't find plugin %s. Sorry." % name)
		return
	
	pn = name.split("/")[-1].replace(".py", "")
	# Due to clashes we need to prepend "Core" onto core plugin names.
	if "-c" in Info.args:
		pn = "Core%s" % pn
	try:
		plugin = imp.load_source(pn, name)
	except:
		Channel.send("There was a problem loading %s. Check the syntax?" % (pn))
		return
	# Helper, Web & Server needs setting to all plugins. (Channel is set per call). 
	if "-l" in Info.args:
		# Libraries.
		if pn == "IRCObjects":
			connection.server = plugin.L_Server(connection)
			for p in connection.plugins.keys():
				p = connection.plugins[p]
				p.Web = plugin.L_Web(connection)
				p.Server = connection.server
				p.Helper = plugin.L_Helper()
			# Okay all done.
		# Lets set the library in the bot
		connection.libraries[pn] = plugin
		Channel.send("Library %s has been reloaded." % (pn))
	elif "-C" in Info.args:
		# config.
		# Has the nick changed?
		if connection.config["nick"] != plugin.networks[connection.name]["nick"]:
			Server.raw("NICK %s" % plugin.networks[connection.name]["nick"])
		connection.config = plugin.networks[connection.name]
		connection.settings = plugin
		Channel.send("Config has been reloaded.")
	elif "-c" in Info.args:
		# core
		connection.core[pn] = plugin
		Channel.send("Core plugin %s has been reloaded" % pn[4:])		
	else:
		connection.plugins[pn] = plugin
		Channel.send("Plugin %s has been reloaded" % pn)

help = "Loads or reloads a plugin"
