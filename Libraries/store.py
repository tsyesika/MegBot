##
# Storage library
##

import os
import json
from types import *

class Store(object):
    def __init__(self, name, data=None):
        # This is to prevent circular deps in imports
        from Configuration import configuration as config

        self.fpath = config["paths"]["databases"]
        if self.fpath[-1] != "/":
            self.fpath += "/" + name
        else:
            self.fpath += name
        if data == None:
            # Tries to load
            if os.path.isfile(self.fpath):
                self._sfile = open(self.fpath)
                data = self._sfile.read()
                data = json.loads(data)
                self._sfile.close()
            else:
                raise IOError
        self._type = type(data)
        self.data = data
        self._sfile = None #holder

    def __repr__(self):
        return self.data.__str__()
    def __str__(self):
        return self.__repr__()
    def __getitem__(self, key):
        if self._type == DictType or self._type == ListType or self._type in StringTypes:
            return self.data[key]
        else:
            raise AttributeError
    def __setitem__(self, key, value):
        if self._type == DictType or self._type == ListType:
            self.data[key] = value
        else:
            raise AttributeError
    def __delitem__(self, key):
        if self._type == DictType or self._type == ListType:
            del self.data[key]
        else:
            raise AttributeError
    def __getslice__(self, i, j):
        if self._type == ListType or self._type in StringTypes:
            return self.data[i:j]
        else:
            raise AttributeError
    def __setslice__(self, i, j, value):
        if self._type == ListType:
            self.data[i:j] = value
        else:
            raise AttributeError
    def __delslice__(self, i, j):
        if self._type == ListType:
            del self.data[i:j]
        else:
            raise AttributeError
    def __contains__(self, key):
        if self._type == DictType or self._type == ListType or self._type in StringTypes:
            return key in self.data
        else:
            raise AttributeError

    def append(self, value):
        if self._type == ListType:
            return self.data.append(value)
        else:
            raise AttributeError
    def pop(self, index=-1):
        if self._type == ListType:
            return self.data.pop(index)
        else:
            raise AttributeError
    def sort(self, cmp=None, key=None, reverse=False):
        if self._type == ListType:
            return self.data.sort(cmp, key, reverse)
        else:
            raise AttributeError
    def index(self, value, start=0, stop=None):
        if self._type == ListType:
            if stop == None:
                return self.data[start:]
            else:
                return self.data[start:stop]
        else:
            raise AttributeError
    def insert(self, index, object):
        if self._type == ListType:
            return self.data.insert(index, object)
        else:
            raise AttributeError
    def count(self, value):
        if self._type == ListType:
            return self.data.count(value)
        else:
            raise AttributeError
    def extend(self, iterable):
        if self._type == ListType:
            return self.data.extend(iterable)
        else:
            raise AttributeError
    def remove(self, value):
        if self._type == ListType:
            return self.data.remove(value)
        else:
            raise AttributeError
    def reverse(self):
        if self._type == ListType:
            return self.data.reverse()
        else:
            raise AttributeError
    def clear(self):
        if self._type == DictType:
            return self.data.clear()
        else:
            raise AttributeError
    def copy(self):
        if self._type == DictType:
            return self.data.copy()
        else:
            raise AttributeError
    def fromkeys(self, seq, value=None):
        if self._type == DictType:
            return self.data.fromkeys(seq, value)
        else:
            raise AttributeError
    def get(self, k, d=None):
        if self._type == DictType:
            return self.data.get(k, d)
        else:
            raise AttributeError
    def has_key(self, k):
        if self._type == DictType:
            return self.data.has_key(k)
        else:
            raise AttributeError
    def items(self):
        if self._type == DictType:
            return self.data.items()
        else:
            raise AttributeError
    def iteritems(self):
        if self._type == DictType:
            return self.data.iteritems()
        else:
            raise AttributeError
    def iterkeys(self):
        if self._type == DictType:
            return self.data.iterkeys()
        else:
            raise AttributeError
    def itervalues(self):
        if self._type == DictType:
            return self.data.itervalues()
        else:
            raise AttributeError
    def keys(self):
        if self._type == DictType:
            return self.data.keys()
        else:
            raise AttributeError
    def pop(self, k, *d):
        if self._type == DictType:
            return self.data.pop(k, d)
        else:
            raise AttributeError
    def popitem(self):
        if self._type == DictType:
            return self.data.popitem()
        else:
            raise AttributeError
    def setdefault(self, k, d=None):
        if self._type == DictType:
            return self.data.setdefault(k, d)
        else:
            raise AttributeError
    def update(self, e, **f):
        if self._type == DictType:
            return self.data.update(e, F)
        else:
            raise AttributeError
    def values(self):
        if self._type == DictType:
            return self.data.values()
        else:
            raise AttributeError
    def viewitems(self):
        if self._type == DictType:
            return self.data.viewitems()
        else:
            raise AttributeError
    def viewkeys(self):
        if self._type == DictType:
            return self.data.viewkeys()
        else:
            raise AttributeError
    def viewvalues(self):
        if self._type == DictType:
            return self.data.viewvalues()
        else:
            raise AttributeError
    
    def save(self, pretty=False, data={}):
        if not data:
            data = self.data

        if pretty:
            foutd = json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '))
        else:
            foutd = json.dumps(data)
        if os.path.isfile(self.fpath):
            os.remove(self.fpath)
        self._sfile = open(self.fpath, "w")
        self._sfile.write(foutd.encode("utf-8"))
        self._sfile.close()
