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
		
		
	