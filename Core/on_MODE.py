def main(bot, message):
    """When a mode is set"""
    try:
        mode = message.split()[3][1:]
        channel = message.split()[2][1:]
        for v1, m in enumerate(mode):
            if m in ["a", "o", "q", "h", "v"]:
                if len(line.split()) <= 3:
                    nick = line.split()[0][1:].split("!")[0]
                else:
                    nick = message.split()[4:][v1]
                if m == "a":
                    bot.channels[channel]["sop"].append(nick)
                elif m == "o":
                    bot.channels[channel]["aop"].append(nick)
                elif m == "h":
                    bot.channels[channel]["hop"].append(nick)
                elif m == "v":
                    bot.channels[channel]["vop"].append(nick)
                elif m == "q":
                    bot.channel[channel]["founder"].append(nick)
    except:
        traceback.print_exc()
