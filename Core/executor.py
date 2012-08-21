import time, threading

def executor(connection, line, plugin):
	if not "times" in dir(connection):
		connection.times = {}
	else:
		clear(connection)
	if not line in connection.times.keys():
		#ignores call if user is executing the same pluign twice before its done
		if line.split()[2] in connection.channels:
			connection.plugins[plugin].Info = connection.libraries["IRCObjects"].Info(line)
			connection.plugins[plugin].Channel = connection.channels[line.split()[2]]
			connection.times[line] = [threading.Thread(target=connection.plugins[plugin].main, args=(connection, line)), time.time(), plugin]
			connection.times[line][0].start()

def clear(connection):
        purge = []
	for plugincall in connection.times:
		if (connection.times[plugincall][1] - time.time()) > 5:
			connection.times[plugincall] #destroy me
		elif not connection.times[plugincall][0].isAlive():
			purge.append(connection.times[plugincall])
	for p in purge:
	        del connection.times[plugincall]
