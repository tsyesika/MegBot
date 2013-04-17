##
#This file is part of MegBot.
#
#   MegBot is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   MegBot is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with MegBot.  If not, see <http://www.gnu.org/licenses/>.
##

import json, urllib2, traceback

def FormTime(time):
    # yeah, i have no fucking clue what was going on here
    # don't expect these variable names to make any sense
    output = ""
    t = 0
    for char_index in range(len(time)):
        if time[char_index] == "+" or time[char_index] == "-":
            t += 1
        if t <= 6 and t > 0:
            t += 1
        elif t > 0:
            t = 0
            output += time[char_index]
        else:
            output += time[char_index]
    return output

def prep_data(data):
    name = data[0]["user"]["screen_name"]
    cid = data[0]["id"]["text"]
    status = data[0]["text"]
    created = FormTime(str(data[0]["created_at"])) + " UTC"
    
    created = datetime.strptime(created, "%a %b %d %H:%M%S %Y %Z")
    dent_time = Helper.HumanTime(created)
    
    return name, cid, status, dent_time

def main(connection):
    if not Info.args:
        nick = Info.nick
    else:
        nick = Info.args[-1]
    try:
        data = urllib2.urlopen("http://identi.ca/api/statuses/user_timeline.json?screen_name=%s" % nick)
        data = data.read()
        data = json.loads(data)
        if data and not ("-g" in Info.args or "-group" in Info.args):
            # this is from the http://status.net/wiki/Twitter-compatible_API
            name, cid, status, dent_time = prep_data(data)
        else:
            data = urllib2.urlopen("http://identi.ca/api/statusnet/groups/timeline/%s.json" % nick)
            data = data.read()
            data = json.loads(data)
            if data:
                name, cid, status, dent_time = prep_data(data)
            else:
                Channel.send("Sorry, they haven't posted on identi.ca")
                return
    except Exception:
        traceback.print_exc()
        Channel.send("An error has occured")
        return
    Channel.send("[%s] %s - %s %s ago - %s http://www.identi.ca/notice/%s" % (Format.Bold(name), status, Format.Bold("Approx:"), dent_time, Format.Bold("Link:"), cid))

help = "Gets the last dent from a specific user/group (or tries your nickname if non is given) from identi.ca (for group support use -g or -group)"
