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

import shelve, time

def main(connection, line):
	"""
	Looks for the last time the user spoke and reports it.
	"""
	if not Info.args:
		Channel.send("Please specify a user")
		return
	
	if Info.args[0] == connection.settings["nick"]:
		Channel.send("o I haven't seen myself, I'm all 1s and 0s")
		return
	
	seen = shelve.open("Seen")
	if Info.args[0] in seen.keys():
		record = seen[Info.args[0]]
		Channel.send("%s said %sin %s at %s" % (
			Info.args[0],
			record["msg"],
			record["channel"],
			time.ctime(record["time"])
		))
	else:
		Channel.send("Can't find %s." % Info.args[0])
	
def on_PRIVMSG(connection, line):
	"""
	Logs this speach.
	"""
	Info = connection.libraries["IRCObjects"].Info(line)
	seen = shelve.open("Seen")
	seen[Info.nick] = {
		"msg":Info.message,
		"time":time.time(),
		"channel":Info.channel,
	}
	seen.sync()
	seen.close()
	
	
def init(connection):
	connection.hooker.register_hook("on_PRIVMSG", on_PRIVMSG)

def unload(connection):
	connection.hooker.unregister_hook("on_PRIVMSG", on_PRIVMSG)

help = "Tells you the last time a specified nick spoke."
