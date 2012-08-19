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
	
	pname = line.split()[-1]
	
	if len(line.split()) > 5:
		if line.split()[4] == "-core" or line.split()[4] == "-c":
			ppath = connection.config.path["coreplugins"]
			pbank = connection.core
			pkey = "Core%s" % pname
		elif line.split()[4] == "-library" or line.split()[4] == "-l":
			ppath = connection.config.path["libraries"]
			pbank = connection.libraries
			pkey = pname
		else:	
			ppath = connection.config.path["plugin"]
			pbank = connection.plugins 
			pkey = pname
	else:
		ppath = connection.config.path["plugin"]
		pbank = connection.plugins
		pkey = pname
	
	if pname.find("/")!=-1:
		try:
			pluginname = pname.split("/")[-1]
			if not pluginname.endswith(".py"):
				pluginname = pluginname + ".py"
			newplugin = open("temp", "w")
			plugin = urllib2.urlopen(line.split()[4])
			newplugin.write(plugin.read())
			newplugin.close()
			shutil.move("temp", ppath + pluginname)
			connection.core["pluginload"].main(connection, plugin)
			Channel.send("Plugin has been retrived & loaded.")
			return
		except:
			Channel.send("Failed to retrive plugin or load.")
	if os.path.isfile("%s%s.py" % (ppath, pname)):
		e = True
		if not pkey in pbank.keys():
			e = False
		if not e and "unloader" in dir(pbank[pkey]):
			pbank[pkey].unloader(connection)
		pbank[pkey] = imp.load_source(pkey, pbank + pname + ".py")
	else:
		Channel.send("Can't find plugin.")
		return
	if e:
		Channel.send("Plugin has been reloaded.")
	else:
		Channel.send("Plugin has been loaded.")

help = "Loads or reloads a plugin (can take a URL)"
