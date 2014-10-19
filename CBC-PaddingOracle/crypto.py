from Crypto.Cipher import AES
import os

	
def pkcs7_pad(plain,blocksize):
	BLOCKSIZE = blocksize #in bytes

	padbyte = BLOCKSIZE - len(plain)%BLOCKSIZE
	plain += chr(padbyte) * padbyte
	return plain

def pkcs7_strip(plain,blocksize):
	BLOCKSIZE = blocksize #in bytes

	numblocks = len(plain)/(BLOCKSIZE) + (1 if len(plain)%BLOCKSIZE else 0)

	newplain = plain[0:(numblocks-1)*BLOCKSIZE]
	padblock = plain[(numblocks-1)*BLOCKSIZE:]
	padbytes = int(padblock[-1:].encode("hex"),16)
	#Validate padding - we should never see a pad end in zero
	if padbytes == 0 or padbytes > BLOCKSIZE:
		raise Exception("PaddingError")
		return ""
	#make sure all the pad bytes make sense
	if padblock[BLOCKSIZE-padbytes:BLOCKSIZE] != chr(padbytes)*padbytes:
		raise Exception("PaddingError")
		return ""
	newplain += padblock[:-padbytes]

	return newplain


def cbc_encrypt(plain, key):

	iv = os.urandom(AES.block_size)
	aes_obj = AES.new(bytes(key), AES.MODE_CBC, iv)
	return iv + aes_obj.encrypt(pkcs7_pad(plain, AES.block_size))

def cbc_decrypt(enc, key):

	iv = enc[:AES.block_size]
	aes_obj = AES.new(bytes(key), AES.MODE_CBC, iv)
	enc_pad = aes_obj.decrypt(enc[AES.block_size:])
	return  pkcs7_strip(enc_pad, AES.block_size)
