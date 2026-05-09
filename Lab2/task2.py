import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import base64
from task1 import pad, unpad
import utility

from Crypto.Cipher import AES



# 16 Bytes
blockSize = 16


# ---------------------------------------------------------------------------
# Part A: AES-128-ECB

def ecbEncrypt(key: bytes, plaintext: bytes) -> bytes:
    # Args: 16 byte AES Key, plaintext
    # Returns: ciphertext with padding

    padded = pad(plaintext)


    # Create new aes cipher using key and encrypt padded text
    aes = AES.new(key, AES.MODE_ECB)
    ciphertext = aes.encrypt(padded)

    return ciphertext


def ecbDecrypt(key: bytes, ciphertext: bytes) -> bytes:
    # Args: 16 byte AES key, ciphertext
    # Returns: plaintext with no padding

    # Check that ciphertext is a full block
    if len(ciphertext) % blockSize != 0:
        print("Ciphertext not a full block")
        return
    
    aes = AES.new(key, AES.MODE_ECB)

    padded = aes.decrypt(ciphertext)

    plaintext = unpad(padded)

    return plaintext


def task2a():

    key = b"CALIFORNIA LOVE!"

    with open("Lab2.TaskII.A.txt", "r") as file:
        contents = file.read()

    # Convert to byte since we know input is base64
    ciphertext = utility.base64ToByte(contents)

    # Decrypt
    plaintext = ecbDecrypt(key, ciphertext)
    
    print(plaintext.decode())


# ---------------------------------------------------------------------------
# Part B: Identify ECB Mode

def checkRepeatingBlocks(data: bytes, blockSize: int = blockSize) -> bool:

    # Returns true if a repeated block is found, false otherwise.
    
    chunks = [data[i:i + blockSize] for i in range(0, len(data), blockSize)]
    return len(chunks) != len(set(chunks))


def task2b():
    

    with open("Lab2.TaskII.B.txt", "r") as file:
        
        # Go through each line in Lab2.TaskII.B.txt
        for line in file:
            
            # Strip newline since not part of msg
            ciphertext = utility.hexToByte(line.strip())
            
            # Splice and skip first 54 bytes (Header)
            splicedCiphertext = ciphertext[54:]

            # If it's ecb encrypted, write to file and return
            if(checkRepeatingBlocks(splicedCiphertext)):
                with open("Lab2TaskII.B.bmp", "wb") as image:
                    image.write(ciphertext)

                return
    
    # Print if no ECB
    print("No ECB Encrypted line in file!")


# ---------------------------------------------------------------------------
# Part C: ECB Cookies

def task2c():
    
    # Usernames for registration
    # AAAAAAAAAAAadmin
    # AAAAAAAAAAAAAAA

    # Paste both auth_tokens from browser dev tools
    tokenOne = input("\nInput first auth_token:").strip()
    tokenTwo = input("Input second auth_token:").strip()

    # Convert hex strings to bytes
    cookie1 = utility.hexToByte(tokenOne)
    cookie2 = utility.hexToByte(tokenTwo)

    # Splice admin and padding from the first cookie
    adminBlock = cookie1[16:32]

    adminCookie = cookie2[:32] + adminBlock


    # Set auth token to admin cookie in devs tools
    print("\nAccount Cookie:", adminCookie)

if __name__ == "__main__":
    task2a()
    task2b()
    task2c()
