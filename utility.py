import base64


# CONVERSIONS ------------------------------------------------------------

def byteToHex(byte):
    
    # Bounds check
    if len(byte) == 0:
        return
    
    return byte.hex()


def hexToByte(hex):

    # Bounds check
    if len(hex) == 0:
        return
    

    return bytes.fromhex(hex)


def base64ToByte(base):
    
    # Bounds check
    if len(base) == 0:
        return
    
    return base64.b64decode(base)


def byteToBase64(byte):
    
    # Bounds check
    if len(byte) == 0:
        return
    
    return base64.b64encode(byte)

def intToByte(num):

    return num.to_bytes(4, byteorder='big')

def byteToInt(byte):

    return int.from_bytes(byte, byteorder='big')

def base64ToInt(base):

    return int(byteToHex(base64ToByte(base)), 16)

def byteToString(byte):

    return byte.decode()

def stringToBase64(string):

    return byteToBase64(string.encode())

# ------------------------------------------------------------------------


def XOR(input: bytes, key: bytes):

    keyCopy = key

    # Only run if length of key doesnt equal length of input
    if len(keyCopy) != len(input):
        # Repeat key until >= len(input)        
        while(len(keyCopy) < len(input)):
            keyCopy *= 2


        # Check if len(keyCopy) is greater than len(input)
        # This will also handle the case where the newKey hah been multiplied
        # to a length that is more than what is needed
        if(len(keyCopy) > len(input)):
            keyCopy = keyCopy[:len(input)]


    result = b''

    for i in range(len(input)):
        result += bytes([input[i] ^ keyCopy[i]])
    
    
    return result
