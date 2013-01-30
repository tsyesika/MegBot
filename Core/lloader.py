# -*- coding: utf-8 -*-
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

"""This will load all the libraries from the directory specified in the config
file. If no directory is specified it'll assume the libraries are in the default
location of "Libraries". The libraries are then loaded. The plugin will always
return type dict ({}). This might be empty if no libraries exist or an invalid
call is made.
"""

from glob import glob
from os import path
from imp import load_source

def main(connection):
    """
    Loads the libraries from Library/ (or what's specified in the config
    under the path dict.
    Returns a dict {library_name : <library instance>}
    """
    libraries = {}
    if "libraries" in connection.config.paths.keys():
        lpath = connection.config.paths["libraries"]
        if not path.isdir(lpath):
            return {}
    else:
        if path.isdir("Libraries"):
            lpath = "Libraries/"
        elif path.isdir("libraries"):
            lpath = "libraries/"
        else:
            return {}
    for plugin in glob(lpath + "*.py"):
        fixed = plugin.replace(lpath, "").replace(".py", "")
        libraries[fixed] = load_source(fixed, plugin)
    return libraries
