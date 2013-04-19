
from Configuration import configuration

class String(str):
	""" 
	This should work a lot like a normal python string but
	we will be handling also the decoding into unicode throughout
	"""

	def __init__(self, *args):
		if args:
			super(String, self).__init__(args)
		else:
			super(String, self).__init__()

		# Now try and decode it.
		encodings = self.__get_encoding()
		decoded = False
		for encoding in encodings:
			try:
				self = self.decode(encoding)
				decoded = True
				break
			except:
				pass

		if not decoded:
			raise TypeError("%s can't be decoded (encoding: %s)" % (self, encodings))


	def __get_encoding(self):
		""" Gets the encodings from the config """
		encodings = []
		
		if "encodings" in configuration and configuration["encodings"]:
			encodings += configuration["encodings"]

		if not "utf-8" in encodings:
			encodings.insert(0, "utf-8")

		return encodings

	def __decode(self, message, encodings):
		""" 
		This will decode message into unicode by trying each 
		encoding in encodings (from encodings[0] -> encodings[len(encodings)])
		and try to decode from them.
		"""
		decoded = False
		for encoding in encodings:
		    try:
		        encoding.decode(encoding)
		        decoded = True
		        break
		    except:
		        pass

		if not decoded:
		    raise Exception("Can't decode '%s', encoding's tried: %s" % (message, encodings))

		return message