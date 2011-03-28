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

from __future__ import division
from math import *
from fractions import gcd
import random, traceback

def lcm(a,b):
    return a*b/gcd(a,b)
def round(a):
	return int(a + 0.5)
def main(connection, line):
	random.seed()
	if len(line.split()) <= 3:
		connection.core["privmsg"].main(connection, line.split()[2], "Plese enter mathamatical expression.")
		return
	
	exp = " ".join(line.split()[4:]).replace("^", "**").replace("x", "*")
	
	##
	# constants
	##
	ln = log1p
	lg = lambda x:log(x, 2)
	log = lambda x:log(x, 10)
	rand = random.randint
	##
	# End of constants
	##
	
	try:
		a = eval(exp)
	except ZeroDivisionError:
		connection.core["privmsg"].main(connection, line.split()[2], "Math Error: Zero Division Error.")
		return
	except:
		connection.core["privmsg"].main(connection, line.split()[2], "Math Error: ?")
		traceback.print_exc()
		return
		
	##
	# Andreas work below
	##
	if a % 1 == 0:
		a = int(a)
	connection.core["privmsg"].main(connection, line.split()[2], "Answer: %s" % a)
		
		
	