MegBot User Documentation
=========================

Introduction
------------

MegBot is a highly flexible IRC bot. Written for python 2.7 under the GPL V3 software licence. Some of the main features are:

- SSL Support
- IPV6 support
- Multiheaded (Multiple network support in a single processs)
- Highly modular
- Threaded
- Plugin support
- Powerful easy to use Libraries
- Updated without restarting bot
- Fully documented

This guide will walk through the options to get an IRC bot up and running, explaining the more advanced features later on. This guide does not explain development, we do have a development guide to explain plugin development and also some of the more core bot aspects needed to develop on the core of MegBot.

Basic Config
------------

You will need to get a basic config written to get your bot online, it will be fairly simple again this is more of a guide at this point than a reference, you will find lower down an explanation of the entire config. This part is just to try and get a bot that is online.

Firstly move config.json.example to config.json an open it in your favourite editor. The very first thing you will notice is the "network" block, this contains all the networks you might want to connect with, you have a block like:

{
    "Network1":{
        some config here
    },
    "Network2":{
        another config here
    },
    "AnotherNetwork":{
        and another config...
    }
}

If you only want to have it connect to one then just do only one block is needed. Most of this will be self explanatory but roughly going through the required options are:

address - this is the address of the IRC server, this can either be a URL or an IP

port - Most IRC servers run on 6667 (and 6697 for ssl), specify your port here.

ident - usually the same as the nickname (though does not have to be)

nick - the nickname you use on the IRC network

realname - the real name of the bot (often same as nickname)

trigger - Usually just one character, this is what the bot will look for to signify someone trying to call a command.

channels - This is a list of channels that you want the bot to join upon connecting.

The rest of the config, unless you know you want to modify it, please ignore it and just leave it as the default.

Running the bot
---------------

Providing you have python 2.7 installed just running

./MegBot

in the terminal should be enough. You should then see it pop into the channels you have specified in the config.


Advanced
========

We are now going to look at each option in some amount of detail and explain each aspect. An important thing to note, if any of this changes during the running of the bot it will be saved back, the bot does not monitor the config for changes however you can reload it with the load plugin while it is running (with -C).


