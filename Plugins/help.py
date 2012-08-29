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

def main(bot, line):
	if not Info.args:
		# Generic list of plugins.
		cout = ""
		amount = len(bot.plugins.keys())-1
		done = False
		for i, x in enumerate(bot.plugins.keys()):
			done = True
			if i == amount:
				cout += " & " + x
			else:
				cout += ", " + x
		if done:
			Channel.send("%s: %s" % (Info.nick, cout[2:]))
		else:
			Channel.send("%s: It seems no plugins are loaded, please speak to the bot admin." % Info.nick)
	else:
		plugin = Info.args[0]
		if plugin in bot.plugins.keys():
			if "help" in dir(bot.plugins[plugin]):
				if type(bot.plugins[plugin].help) == type(range):
					# It's a function
					bots.plugins[plugin].help(bot, line)
				elif type(bot.plugins[plugin].help) == type(""):
					# It's a string
					Channel.send("%s: %s" % (Info.nick, bot.plugins[plugin].help))
			else:
				Channel.send("%s: Can't find any help for %s." % (Info.nick, plugin))
		else:
			Channel.send("%s: Can't find plugin %s." % (Info.nick, plugin))

help = "Displays a list of plugins or if a plugin is specified tries to get the help for that plugin"
