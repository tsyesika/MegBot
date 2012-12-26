def main(bot, message):
    """Handles the PINGS"""
    if message[0] == "PING":
        bot.core["Coreraw"].main(bot, "PONG %s" % message[1])
