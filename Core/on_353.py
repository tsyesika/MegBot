def main(bot, message):
    """Names on joining of a channel"""
    channel = message.split("#")[1].split()[0]
    nicks = message.split(":")[2].split()
    bot.channels[channel] = {"all":[], "hop":[], "sop":[], "aop":[], "vop":[], "non":[], "founder":[]}
    for nick in nicks:
        if nick[0] in ["+", "&", "@", "%", "~"]:
            bot.channels[channel][bot.config.permissions[nick[0]]].append(nick[1:])
            bot.channels[channel]["all"].append(nick[1:])
        else:
            bot.channels[channel]["non"].append(nick)
            bot.channels[channel]["all"].append(nick)