def main(bot, message):
    """
    This will tell the bot to reconnect by setting a variable
    inside the bot to be False, this will cause it to run through the reconnection.:
    """
    if message.split()[0].split("!")[0][1:] == bot.settings["nick"]:
        # Bot quit.
        # initate reconnect.
        bot.running = False
