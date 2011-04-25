##
# will change before 0.06 is released
##


networks = {
	"MegNet":{
		"address":"irc.megworld.co.uk",
		"port":6667,
		"nick":"MegBot",
		"ident":"MegBot",
		"realname":"MegBot",
		"ipv6":False,
		"ssl":False,
		"trigger":"",
		"NSPassword":"nickservpass",
		"commands":[],
		"modes":["b"],
		"channels":["#bots", "#megworld"]
	},
	"Freenode":{
		"address":"irc.freenode.net",
		"port":6667,
		"nick":"",
		"ident":"",
		"realname":"",
		"trigger":"",
		"ipv6":False,
		"ssl":False,
		"NSPassword":"pass",
		"commands":[],
		"modes":["b"],
		"channels":[],
		"active":False #optional (if set to false will disable this network from connecting.)
	}
}

permissions = {
	"~":"founder",
	"&":"sop",
	"@":"aop",
	"%":"hop",
	"+":"vop"
}

paths = {
	"plugin":"Plugins/",
	"coreplugins":"CorePlugins/",
	"logs":"Logging/",
	"databases":"Databases/"
}