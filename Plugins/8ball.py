import random

def main(connection, line):
	connection.core["privmsg"].main(connection, line.split()[2], random.choice(["sure", "yerp", "no", "nope", "I'm not sure", "I'm to tired right now, ask later."]))

def initalisation(connection):
	pass