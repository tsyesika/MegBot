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

def main(connection, line):
	if len(line.split()) <= 3:
		Channel.send("Please enter plugin name.")
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
			connection.core["pluginload"].main(connection, plugin)
			Channel.send("Plugin has been retrived & loaded.")
			return
		except:
			Channel.send("Failed to retrive plugin or load.")
	if os.path.isfile(connection.config.paths["plugin"] + line.split()[4] + ".py"):
		if "unloader"  in dir(connection.plugins[line.split()[4]]):
			connection.plugins[line.split()[4]].unloader(connection)
		connection.plugins[line.split()[4]] = imp.load_source(line.split()[4], connection.config.paths["plugin"] + line.split()[4] + ".py")
	else:
		Channel.send("Can't find plugin.")
		return
	if line.split()[4] in connection.plugins.keys():
		Channel.send("Plugin has been reloaded.")
	else:
		Channel.send("Plugin has been loaded.")
