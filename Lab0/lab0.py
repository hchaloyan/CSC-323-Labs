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

# ------------------------------------------------------------------------


def XOR(input: bytes, key: bytes):

    keyCopy = key

    # Only run if length of key doesnt equal length of input
    if len(keyCopy) != len(input):
        # Repeat key until >= len(input)        
        while(len(keyCopy) < len(input)):
            keyCopy *= 2
            print(keyCopy)


        # Check if len(keyCopy) is greater than len(input)
        # This will also handle the case where the newKey hah been multiplied
        # to a length that is more than what is needed
        if(len(keyCopy) > len(input)):
            keyCopy = keyCopy[:len(input)]
            print(keyCopy)


    return input.replace(keyCopy, b'')
    


def main():


    # Tests for encoders and decoders ------------------------------------

    var = b'Hello Chat'
    
    
    hexFromByte = byteToHex(var)

    print("PRINTING HEX FROM BYTE: ", hexFromByte)

    byteFromHex = hexToByte(hexFromByte)

    print("PRINTING BYTE FROM HEX: ", byteFromHex)

    
    var2 = b'SGVsbG8gQ2hhdA=='

    byteFromBase64 = base64ToByte(var2)

    print("PRITING BYTE FROM BASE64: ", byteFromBase64)

    base64FromByte = byteToBase64(byteFromBase64)

    print("PRINTING BASE64 FROM BYTE: ", base64FromByte)


    # --------------------------------------------------------------------

    # XOR Implementation Test

    byte1 = b'Hell'
    key1 = b'Hello'

    print(XOR(byte1, key1))





if __name__=="__main__":
    main()