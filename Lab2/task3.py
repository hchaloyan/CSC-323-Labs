import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import base64
from task1 import pad, unpad
import utility
from Crypto.Cipher import AES




# 16 Bytes
blockSize = 16


# ---------------------------------------------------------------------------
# Part A: Implement CBC Mode

def cbcEncrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:


    # Args: 16 Byte AES Key, 16 Byte Initialization Vector, Plaintext
    # Returns: Initialization vector in front of ciphertext



    padded = pad(plaintext)

    # Split into 16-byte blocks
    blocks = []
    for i in range(0, len(padded), blockSize):
        
        chunk = padded[i : i + blockSize]
        
        blocks.append(chunk)

    ciphertext = b""
    prevBlock = iv

    for block in blocks:
        # XOR block with previous ciphertext block
        xorBlock = utility.XOR(block, prevBlock)

        # Used aes ECB because task2's implementation had padding
        aes = AES.new(key, AES.MODE_ECB)
        cipherBlock = aes.encrypt(xorBlock)

        ciphertext += cipherBlock
        prevBlock = cipherBlock

    # Prepend IV to allow decryption
    return iv + ciphertext


def cbcDecrypt(key: bytes, ciphertext: bytes) -> bytes:
    
    # Ciphertext must be a whole number of blocks
    if len(ciphertext) % blockSize != 0:
        print("Not a whole number of blocks")
        return

    # Split off IV from the front
    iv = ciphertext[:blockSize]

    
    blocks = []
    
    # SKIP FIRST BLOCK
    for i in range(blockSize, len(ciphertext), blockSize):
        chunk = ciphertext[i : i + blockSize]
        blocks.append(chunk)

    plaintext = b""
    prevBlock = iv

    for block in blocks:

        # Decrypt single block using AES-ECB
        aes = AES.new(key, AES.MODE_ECB)
        
        
        decrypted = aes.decrypt(block)

        # XOR with previous ciphertext block
        plaintextBlock = utility.XOR(decrypted, prevBlock)

        plaintext += plaintextBlock
        prevBlock = block

    return unpad(plaintext)


def task3a():


    key = b"MIND ON MY MONEY"
    iv  = b"MONEY ON MY MIND"

    with open("Lab2.TaskIII.A.txt", "r") as file:
        contents = file.read()
    
    ciphertext = utility.base64ToByte(contents)

    plaintext = cbcDecrypt(key, ciphertext)

    print(plaintext.decode())


# ---------------------------------------------------------------------------
# Part B: CBC Cookies

def task3b():
    
    # LOG IN WITH
    # A
    
    # cookie = "user=" + urllib.parse.quote_plus(user) + "&uid=" + str(userid) + "&role=" + role
    # 'user=a&uid=1' '0x00' '0x00' '0x00' '0x04' | &role=user '0x00' '0x00' '0x00' '0x00' '0x00' '0x06'
    # 'user=a&uid=1' '0x00' '0x00' '0x00' '0x04' | &role=admin '0x00' '0x00' '0x00' '0x00' '0x05'

    # https://medium.com/@olyhossen10/breaking-aes-cbc-the-bit-flipping-attack-to-gain-admin-access-a8d64040e962

    token = input("\nInput auth_token:").strip()
    cookie = utility.hexToByte(token)
    
    currentBlock = b'&role=user\x00\x00\x00\x00\x00\x06'
    goalBlock    = b'&role=admin\x00\x00\x00\x00\x00\x05'
    
    ivBlock = cookie[0:16]
    block1 = cookie[16:32]
    block2  = cookie[32:48]

    offset = utility.XOR(currentBlock, goalBlock)
    
    modifiedBlock1 = utility.XOR(block1, offset) 


    adminCookie = utility.byteToHex(ivBlock + modifiedBlock1 + block2)
    
    print("Account Cookie:", adminCookie)


if __name__ == "__main__":
    task3a()
    task3b()
