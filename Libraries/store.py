##
# Storage library
##

import os, config, json

class Store():
	def __init__(self, name, data=None):
		self.fpath = config.paths["databases"]
		if self.fpath[-1] != "/":
			self.fpath += "/" + name
		else:
			self.fpath += name
		if data == None:
			# Tries to load
			if os.path.isfile(self.fpath):
				self.__sfile = open(self.fpath)
				data = self.__sfile.read()
				data = json.loads(data)
				self.__sfile.close()
			else:
				raise IOError
		self.__type = type(data)
		self.data = data
		self.__sfile = None #holder

	def __repr__(self):
		return self.data.__str__()
	def __str__(self):
		return self.__repr__()
	def __getitem__(self, key):
		if self.__type == type({}) or self.__type == type([]) or self.__type == type(""):
			return self.data[key]
		else:
			raise AttributeError
	def __setitem__(self, key, value):
		if self.__type == type({}) or self.__type == type([]):
			self.data[key] = value
		else:
			raise AttributeError
	def __delitem__(self, key):
		if self.__type == type({}) or self.__type == type([]):
			del self.data[key]
		else:
			raise AttributeError
	def __getslice__(self, i, j):
		if self.__type == type([]) or self.__type == type(""):
			return self.data[i:j]
		else:
			raise AttributeError
	def __setslice__(self, i, j, value):
		if self.__type == type([]):
			self.data[i:j] = value
		else:
			raise AttributeError
	def __delslice__(self, i, j):
		if self.__type == type([]):
			del self.data[i:j]
		else:
			raise AttributeError
	def __contains__(self, key):
		if self.__type == type([]) or self.__type == type(""):
			return key in self.data
		else:
			raise AttributeError
		
	def append(self, value):
		if self.__type == type([]):
			return self.data.append(value)
		else:
			raise AttributeError
	def pop(self, index=-1):
		if self.__type == type([]):
			return self.data.pop(index)
		else:
			raise AttributeError
	def sort(self, cmp=None, key=None, reverse=False):
		if self.__type == type([]):
			return self.data.sort(cmp, key, reverse)
		else:
			raise AttributeError
	def index(self, value, start=0, stop=None):
		if self.__type == type([]):
			if stop == None:
				return self.data[start:]
			else:
				return self.data[start:stop]
		else:
			raise AttributeError
	def insert(self, index, object):
		if self.__type == type([]):
			return self.data.insert(index, object)
		else:
			raise AttributeError
	def count(self, value):
		if self.__type == type([]):
			return self.data.count(value)
		else:
			raise AttributeError
	def extend(self, iterable):
		if self.__type == type([]):
			return self.data.extend(iterable)
		else:
			raise AttributeError
	def remove(self, value):
		if self.__type == type([]):
			return self.data.remove(value)
		else:
			raise AttributeError
	def reverse(self):
		if self.__type == type([]):
			return self.data.reverse()
		else:
			raise AttributeError
	def clear(self):
		if self.__type == type({}):
			return self.data.clear()
		else:
			raise AttributeError
	def copy(self):
		if self.__type == type({}):
			return self.data.copy()
		else:
			raise AttributeError
	def fromkeys(self, seq, value=None):
		if self.__type == type({}):
			return self.data.fromkeys(seq, value)
		else:
			raise AttributeError
	def get(self, k, d=None):
		if self.__type == type({}):
			return self.data.get(k, d)
		else:
			raise AttributeError
	def has_key(self, k):
		if self.__type == type({}):
			return self.data.has_key(k)
		else:
			raise AttributeError
	def items(self):
		if self.__type == type({}):
			return self.data.items()
		else:
			raise AttributeError
	def iteritems(self):
		if self.__type == type({}):
			return self.data.iteritems()
		else:
			raise AttributeError
	def iterkeys(self):
		if self.__type == type({}):
			return self.data.iterkeys()
		else:
			raise AttributeError
	def itervalues(self):
		if self.__type == type({}):
			return self.data.itervalues()
		else:
			raise AttributeError
	def keys(self):
		if self.__type == type({}):
			return self.data.keys()
		else:
			raise AttributeError
	def pop(self, k, *d):
		if self.__type == type({}):
			return self.data.pop(k, d)
		else:
			raise AttributeError
	def popitem(self):
		if self.__type == type({}):
			return self.data.popitem()
		else:
			raise AttributeError
	def setdefault(self, k, d=None):
		if self.__type == type({}):
			return self.data.setdefault(k, d)
		else:
			raise AttributeError
	def update(self, e, **f):
		if self.__type == type({}):
			return self.data.update(e, F)
		else:
			raise AttributeError
	def values(self):
		if self.__type == type({}):
			return self.data.values()
		else:
			raise AttributeError
	def viewitems(self):
		if self.__type == type({}):
			return self.data.viewitems()
		else:
			raise AttributeError
	def viewkeys(self):
		if self.__type == type({}):
			return self.data.viewkeys()
		else:
			raise AttributeError
	def viewvalues(self):
		if self.__type == type({}):
			return self.data.viewvalues()
		else:
			raise AttributeError
	def save(self):
		foutd = json.dumps(self.data)
		if os.path.isfile(self.fpath):
			os.remove(self.fpath)
		self.__sfile = open(self.fpath, "w")
		self.__sfile.write(foutd)
		self.__sfile.close()
