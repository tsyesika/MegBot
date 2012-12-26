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

import urllib2, urllib, re

# predefined stuff
currancies = {
         "Algerian Dinar":"DZD",
         "Namibian Dollar":"NAD",
         "Qatari Rial":"QAR",
         "Egyptian Pound":"EGP",
         "Bulgarian Lev":"BGN",
         "Bolivian Boliviano":"BOB",
         "Danish Krone":"DKK",
         "Botswanan Pula":"BWP",
         "Lebanese Pound":"LBP",
         "Tanzanian Shilling":"TZS",
         "Vietnamese Dong":"VND",
         "Malaysian Ringgit":"MYR",
         "Cayman Islands Dollar":"KYD",
         "Ukrainian Hryvnia":"UAH",
         "Jordanian Dinar":"JOD",
         "Saudi Riyal":"SAR",
         "Euro":"EUR",
         "Hong Kong Dollar":"HKD",
         "Swiss Franc":"CHF",
         "Salvadoran Coln":"SVC",
         "Croatian Kuna":"HRK",
         "Thai Baht":"THB",
         "Brunei Dollar":"BND",
         "Uruguayan Peso":"UYU",
         "Nicaraguan Crdoba":"NIO",
         "Moroccan Dirham":"MAD",
         "Philippine Peso":"PHP",
         "South African Rand":"ZAR",
         "Paraguayan Guarani":"PYG",
         "Nigerian Naira":"NGN",
         "Costa Rican Coln":"CRC",
         "United Arab Emirates Dirham":"AED",
         "Estonian Kroon":"EEK",
         "Sri Lankan Rupee":"LKR",
         "Slovak Koruna":"SKK",
         "Pakistani Rupee":"PKR",
         "Hungarian Forint":"HUF",
         "Romanian Leu":"RON",
         "Ugandan Shilling":"UGX",
         "Jamaican Dollar":"JMD",
         "Seychellois Rupee":"SCR",
         "Turkish Lira":"TRY",
         "Bangladeshi Taka":"BDT",
         "Yemeni Rial":"YER",
         "CFA Franc BCEAO":"XOF",
         "Netherlands Antillean Guilder":"ANG",
         "Norwegian Krone":"NOK",
         "Indian Rupee":"INR",
         "Mexican Peso":"MXN",
         "Czech Republic Koruna":"CZK",
         "Nepalese Rupee":"NPR",
         "Colombian Peso":"COP",
         "Mauritian Rupee":"MUR",
         "Indonesian Rupiah":"IDR",
         "Honduran Lempira":"HNL",
         "Fijian Dollar":"FJD",
         "Peruvian Nuevo Sol":"PEN",
         "US Dollar":"USD",
         "Israeli New Sheqel":"ILS",
         "Dominican Peso":"DOP",
         "Moldovan Leu":"MDL",
         "Swedish Krona":"SEK",
         "Zambian Kwacha":"ZMK",
         "Maldivian Rufiyaa":"MVR",
         "Australian Dollar":"AUD",
         "South Korean Won":"KRW",
         "Venezuelan Bolvar":"VEF",
         "Chilean Peso":"CLP",
         "Lithuanian Litas":"LTL",
         "Kazakhstani Tenge":"KZT",
         "Russian Ruble":"RUB",
         "Trinidad and Tobago Dollar":"TTD",
         "Omani Rial":"OMR",
         "Brazilian Real":"BRL",
         "Polish Zloty":"PLN",
         "Kenyan Shilling":"KES",
         "Macedonian Denar":"MKD",
         "British Pound Sterling":"GBP",
         "New Taiwan Dollar":"TWD",
         "Canadian Dollar":"CAD",
         "Kuwaiti Dinar":"KWD",
         "Papua New Guinean Kina":"PGK",
         "Singapore Dollar":"SGD",
         "Uzbekistan Som":"UZS",
         "Chinese Yuan":"CNY",
         "Sierra Leonean Leone":"SLL",
         "Tunisian Dinar":"TND",
         "New Zealand Dollar":"NZD",
         "Latvian Lats":"LVL",
         "Argentine Peso":"ARS",
         "Serbian Dinar":"RSD",
         "Bahraini Dinar":"BHD",
         "Japanese Yen":"JPY"
}
currancy_switch = {}
for c in currancies:
    currancy_switch[currancies[c].lower()] = c
for x in currancies.keys():
    currancies[x.lower()] = currancies[x]
    del currancies[x]


def fixurl(url):
    url = url.replace("+", "%2B")
    url = url.replace("/", "%2F")
    url = url.replace("(", "%28")
    url = url.replace(")", "%29")
    url = url.replace(" ", "+")
    return url

def main(connection, line):
    global currancy_switch, currancies
    if not Info.args:
        Channel.send("Plese enter mathamatical expression.")
        return
    exp = " ".join(Info.args)
    lexp = exp.lower()
    # Try and figure out what it is first...
    # Conversion?
    if lexp.find("to")!=-1:
        #currancy?
        tpart = lexp.split("to")
        a, tpart[0]  = tuple(tpart[0].split(" ")[:2])
        tpart = [tpart[0].replace(" ", ""), tpart[1].replace(" ", "")]
        if (tpart[0] in currancies.keys()):
            tpart[0] = currancies[tpart[0]].lower()
        if (tpart[1] in currancies.keys()):
            tpart[1] = currancies[tpart[1]].lower()
        if (tpart[0] in currancy_switch.keys()) and (tpart[1] in currancy_switch.keys()):
            google = urllib2.Request("http://www.google.com/finance/converter?a=%s&from=%s&to=%s" % (a, tpart[0].upper(), tpart[1].upper()))
            google.add_header("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel; Mac OS X 10_6_6; en-gb) AppleWebKit/533.19.4 (KHTML, like Gecko Vesion/5.0.3")
            google = urllib2.urlopen(google)
            source = google.read()
            total = re.findall("<div id=currency_converter_result>(.+?)<span class=bld>(.+?)</span>", source)[0][1]
            Channel.send("%s %s = %s %s" % (a, currancy_switch[tpart[0]], total.split(" ")[0], currancy_switch[tpart[1]]))
            return 
    
    google = urllib2.Request("http://google.com/m?q=%s" % fixurl(exp))
    google.add_header("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-gb) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3")
    google = urllib2.urlopen(google)
    source = google.read()[5000:]
    #Channel.send("%s" % source[source.find("999 + 999")-30:source.find("2 + 2 = 4")+20])
    #f = open("test.html", "w")
        #f.write(source)
        #f.close()
    a = re.findall("<span class=\"sifhoi\">(.+?)</span> </d", source)
    a = a[0].replace("&nbsp;", ",")
    try:
        Channel.send("%s" % a)
    except:
        Channel.send("Math Error: ?")
        
help = "Uses google to do calculations or conversions"
