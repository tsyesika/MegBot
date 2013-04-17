    # -*- coding: utf-8 -*-

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

import urllib2, time
import xml.etree.ElementTree as etree
import Libraries.store as store

def main(connection):
    """
    Uses the Yahoo API with the (so far) undocumented Weoid API MegWorld provides.
    This will check the spelling of the entered place, look up it's Weoid and then the weather for said place.
    The Yahoo weather documentation is:
    http://developer.yahoo.com/weather/
    The MegWorld Weoid API takes the argument place as a GET argument.

    Todo:
    - Speed improvements? (possibly add caching?)
    """
    if not Info.args:
        Channel.send(u"Please specify a place")
        return

    # Checks the spelling of said place.
    new_spelling = Web.SpellCheck(" ".join(Info.args))
    different = False
    if new_spelling != " ".join(Info.args):
        # They're different (lets add (corrected from onto it))
        different = u"(Changed from: %s)" % " ".join(Info.args)
    else:
        different = u""

    # Lets replace , with +
    new_spelling = Web.WebSafeString(new_spelling)

    # first lets look up it's woeid.
    woeid = urllib2.urlopen("http://api.megworld.co.uk/WoeidLookup/lookup.php?format=xml&place=%s" % (new_spelling))
    woeid = etree.fromstring(woeid.read())

    if int(woeid.attrib["{http://www.yahooapis.com/v1/base.rng}total"]) == 0:
        Channel.send(u"Sorry, couldn't find that place.")
        return

    woeid = woeid.find('{http://where.yahooapis.com/v1/schema.rng}place/{http://where.yahooapis.com/v1/schema.rng}woeid').text

    try:
        cache = store.Store("WeatherCache")
    except IOError:
        cache = store.Store("WeatherCache", {})

    current_time = time.time()

    try:
        condition, wind, location, atmos, cache_time = cache[woeid]

        condition = etree.fromstring(condition)
        wind = etree.fromstring(wind)
        atmos = etree.fromstring(atmos)

        # check to see if cache is older than 1 hour
        if (current_time - cache_time) > 3600:
            raise KeyError #cheap hack :P

        print "Using cache for %s" % woeid

    except KeyError:
        # Either there's no cache or it's out of date
        # Let's lookup the weather using yahoo's weather API.
        weather = urllib2.urlopen("http://weather.yahooapis.com/forecastrss?w=%s" % woeid)
        weather = etree.fromstring(weather.read())

        # Grab XML elements from tree
        # (prefixes don't seem to be working in my version of python)
        condition = weather.find("channel/item/{http://xml.weather.yahoo.com/ns/rss/1.0}condition")
        wind = weather.find("channel/{http://xml.weather.yahoo.com/ns/rss/1.0}wind")
        atmos = weather.find("channel/{http://xml.weather.yahoo.com/ns/rss/1.0}atmosphere")

        # Location is given to us as in the form of city, region, country, but region
        # is sometimes "", so we do this:
        location = weather.find("channel/{http://xml.weather.yahoo.com/ns/rss/1.0}location")
        locate = []
        try:
            for i in ["city", "region", "country"]:
                tmp = location.get(i)
                if tmp:
                    locate.append(tmp)
            location = ", ".join(locate)
            location = location.encode("utf-8") #quick hack in case of UNICODES :O
            location = Format.Bold(location)
        except AttributeError:
            location = None


        # Store weather in cache
        try:
            cache[woeid] = (etree.tostring(condition), etree.tostring(wind), location, etree.tostring(atmos), current_time)
            cache.save()
        except Exception:
            pass

    # If any of these haven't been set, we have incomplete data
    if None in [location, condition, wind, atmos]:
        place = " ".join(Info.args)
        Channel.send(u"Incomplete weather data recieved for %s (%s), please contact weather station", place, woeid)
        return

    # Okay now we need to convert F to C & K
    celsius = int((float(condition.get("temp")) - 32) / (9 / 5.) + .5)
    kelvin = celsius + 273

    # Convert wind speed from mph to kmph
    kmph = int(int(wind.get("speed")) * 1.60934 + .5)

    # Send it all to the channel
    Channel.send("[%s] Condition: %s | Temp: %sC/%sF/%sK | Humidity: %s%% | Wind Speed %smph/%skmph %s",
     location, condition.get("text"), celsius, condition.get("temp"), kelvin, atmos.get("humidity"), wind.get("speed"), kmph, different)

help = u"Uses Yahoo's weather API to give you the weather for the location specified."
