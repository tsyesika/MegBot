import time, traceback
def main(bot, message):
    """End of MOTD"""
    print bot.core
    for channel in bot.settings["channels"]:
        bot.core["Corejoin"].main(bot, channel)
    if bot.settings["NSPassword"]:
        bot.core["Coreprivmsg"].main(bot, "NickServ", "identify %s" % bot.settings["NSPassword"])
    time.sleep(2)
    for cmd in bot.settings["commands"]:
        bot.core["Coreraw"].main(bot, cmd)
