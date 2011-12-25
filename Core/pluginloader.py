import glob, imp, os

def main(connection):
	for g in glob.glob(connection.config.paths["plugin"] + "*.py"):
		if os.name == "nt":
			connection.plugins[g.replace(connection.config.paths["plugin"][:-1], "").replace(".py", "")] = imp.load_source(g.replace(connection.config.paths["plugin"][:-1], "").replace(".py", ""), g) 
		else:
			connection.plugins[g.replace(connection.config.paths["plugin"], "").replace(".py", "")] = imp.load_source(g.replace(connection.config.paths["plugin"], "").replace("*.py", ""), g)
	for plugin in connection.plugins.keys():
		if "init" in dir(connection.plugins[plugin]):
			connection.plugins[plugin].init(connection)
