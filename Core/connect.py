from time import sleep
def main(connection):
    """ Connects to irc (by setting up socket and passing info to ircd) """
    if connection.settings["ssl"]:
        import ssl # Moved here as ssl is excluded on some python installs distributed with some linuxs 
        connection.sock = ssl.wrap_socket(connection.sock)
    connected = False
    while not connected:
        try:
            connection.sock.connect((connection.settings["address"], connection.settings["port"]))
            connected = True
        except:
            timeout = 10 # default, 10 seconds.
            if "timeout" in connection.settings.keys():
                timeout = connection.settings["timeout"]
            elif "timeout" in dir(connection.config):
                timeout = connection.config.timeout
            sleep(timeout)
    connection.core["Coreraw"].main(connection, "NICK %s" % connection.settings["nick"])
    connection.core["Coreraw"].main(connection, "USER 8 * %s :%s" % (connection.settings["ident"], connection.settings["realname"]))
    connection.running = True
    return
def initalise():
    """ Called on initalisation"""
    pass
