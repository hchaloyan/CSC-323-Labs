import os, hashlib

class KeyedMAC:
	def __init__(self):
		self.key = os.urandom(hashlib.sha1().digest_size)
		#self.key = "YELLOW SUBMARINE"

	def mac_sha1_sign(self, key, msg):
		return hashlib.sha1(key.encode("hex") + msg).digest()

	def mac_sha1_verify(self, key, msg, tag):
		tag_new = hashlib.sha1(key.encode("hex") + msg).digest()

		#An obvious check
		if len(tag) != len(tag_new):
			return False
		
		#To avoid timing attacks, be sure to check all the bytes
		result = 0
		for x, y in zip(tag, tag_new):
			result |= ord(x) ^ ord(y)
		return result == 0

	def verify_post(self, msg, tag):
		try:
			ret = self.mac_sha1_verify(self.key, msg, tag.decode("hex"))
		except:
			ret = False
		return ret
	
	def mac_post(self, msg):
		return self.mac_sha1_sign(self.key, msg).encode("hex")