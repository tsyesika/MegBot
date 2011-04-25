import glob, imp

def main(connection):
	for g in glob.glob(connection.config.paths["plugin"] + "*.py"):
		connection.plugins[g.replace(connection.config.paths["plugin"], "").replace(".py", "")] = imp.load_source(g.replace(connection.config.paths["plugin"], "").replace("*.py", ""), g)
