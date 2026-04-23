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


        # Check if len(keyCopy) is greater than len(input)
        # This will also handle the case where the newKey hah been multiplied
        # to a length that is more than what is needed
        if(len(keyCopy) > len(input)):
            keyCopy = keyCopy[:len(input)]


    result = b''

    for i in range(len(input)):
        result += bytes([input[i] ^ keyCopy[i]])
    
    
    return result

# TASK I -----------------------------------------------------------------

def task1():
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

# TASK IIA ---------------------------------------------------------------

def task2A():
    # XOR Implementation Test

    byte1 = b'Hello'
    key1 = b'He'

    

    print("PRINTING XOR RESULT FROM B'Hello' and b'He': ", XOR(byte1, key1))

# TASK IIB ---------------------------------------------------------------


# Top frequent characters, most -> least
LETTER_FREQ = b' etaoinshrdlu'

# Assign scores based on how close the bytes are to the frequency in the english language
def scoreText(text: bytes) -> int:
    score = 0
    for byte in text:
        # Increment 
        if byte in LETTER_FREQ:
            score += 1
    return score

# XORs against every single byte
def breakSingleByteXOR(ciphertext: bytes):
    
    # Initialize "best" variables for each category we will be returning
    bestScore = -1
    bestPlaintext = None
    bestKey = None

    for k in range(256):
        # Convert integer to its byte equivalent
        key = bytes([k])

        plaintext = XOR(ciphertext, key)

        # If score is better than what we have so far, replace
        if scoreText(plaintext) > bestScore:
            bestScore = scoreText(plaintext)
            bestPlaintext = plaintext
            bestKey = key
    
    return bestPlaintext, bestKey, bestScore
        

def task2B():


    lines = open('Lab0.TaskII.B.txt', 'r').read().splitlines()

    bestScore = -1
    output = None

    for line in lines:
        # Convert line to byte
        ciphertext = hexToByte(line)
        plaintext, key, score = breakSingleByteXOR(ciphertext)
        
        # Update bestScore if new score is higher
        if score > bestScore:
            bestScore = score
            output = (plaintext, key)

    print("Key:", output[1])
    print("Plaintext:", output[0])

# TASK IIC ---------------------------------------------------------------

def calculateNumDifferingBits(bytes1: bytes, bytes2: bytes) -> int:
    score = 0
    resultingBytes = XOR(bytes1, bytes2)
    for byte in resultingBytes:
        # Convert to binary, count the number of 1s (Differing bits, since XORed)
        score += bin(byte).count('1')
    return score

# Brute forces key length
def findKeyLength(ciphertext: bytes) -> int:
    bestLength = None
    bestScore = float('inf')

    for keyLength in range(2, len(ciphertext)):
        
        block1 = ciphertext[0:keyLength]
        block2 = ciphertext[keyLength:keyLength * 2]
        
        numDifferingBits = calculateNumDifferingBits(block1, block2)
        
        if (numDifferingBits / keyLength) < bestScore:
            bestScore = numDifferingBits / keyLength
            bestLength = keyLength

    return bestLength


def task2C():

    input = open('Lab0.TaskII.C.txt', 'r').read().strip()

    # Convert to byte, since input is in base64
    ciphertext = base64ToByte(input)

    keyLength = findKeyLength(ciphertext)

    print("Key Length Guess:", keyLength)

    # Empty
    key = b''


    for i in range(keyLength):
        
        
        # Get bytes associated with its key byte -------------------

        block = b''
        j = i

        while j < len(ciphertext):
            block += bytes([ciphertext[j]])
            j += keyLength


        plaintext, keyByte, score = breakSingleByteXOR(block)

        # Add key byte to key
        key += keyByte

    print("Key:", key)
    print("Plaintext:", XOR(ciphertext, key))

# TASK IID ---------------------------------------------------------------

# Top frequent characters, most -> least
ENGLISH_FREQ = {
    'E': 13, 'T': 9, 'A': 8, 'O': 8, 'I': 7, 'N': 7,
    'S': 6, 'H': 6, 'R': 6, 'D': 4, 'L': 4, 'U': 3,
    'C': 3, 'M': 2, 'W': 2, 'F': 2, 'G': 2, 'Y': 2,
    'P': 2, 'B': 1, 'V': 1, 'K': 1, 'J': 1, 'X': 1,
    'Q': 1, 'Z': 1
}

def scoreString(text: str) -> int:
    score = 0
    for char in text:
        if char in ENGLISH_FREQ:        
            score += ENGLISH_FREQ[char]
    
    return score

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def breakVigenere(ciphertext: str) -> str:
    

    candidates = []
    
    # Try key lengths and pick the one that gives the best score
    for keyLength in range(1, 20):
        
        keyCandidate = ''
        
        # Find the best shift for each key position
        for i in range(keyLength):
            
            # Get bytes associated with its key byte
            block = ciphertext[i::keyLength]
            
            bestScore = -1
            bestShift = None
            
            # Pick best shift from 26 shifts
            for shift in range(26):
                decryptedBlock = ''
                for char in block:
                    decryptedChar = ALPHABET[(ALPHABET.index(char) - shift) % 26]
                    decryptedBlock += decryptedChar

                # Replace if new score better
                if scoreString(decryptedBlock) > bestScore:
                    bestScore = scoreString(decryptedBlock)
                    bestShift = shift
            
            keyCandidate += ALPHABET[bestShift]
        
        plaintext = ''
        for i in range(len(ciphertext)):
            shift = ALPHABET.index(keyCandidate[i % len(keyCandidate)])
            plaintext += ALPHABET[(ALPHABET.index(ciphertext[i]) - shift) % 26]
        
        candidates.append((scoreString(plaintext), keyCandidate, plaintext))

        
    # Sort and print candidates, only top 5 likely
    candidates.sort(reverse=True)
    for score, key, plaintext in candidates[:5]:
        print((f"Key: {key}, plaintext: {plaintext}"))



def task2D():

    ciphertext = open('Lab0.TaskII.D.txt', 'r').read().strip()

    breakVigenere(ciphertext)

# MAIN -------------------------------------------------------------------

def main():

    print("\n\nRUNNING TASK I\n\n")
    task1()

    print("\n\nRUNNING TASK IIA\n\n")
    task2A()

    print("\n\nRUNNING TASK IIB\n\n")
    task2B()

    print("\n\nRUNNING TASK IIC\n\n")
    task2C()

    print("\n\nRUNNING TASK IID\n\n")
    task2D()

# ------------------------------------------------------------------------

if __name__=="__main__":
    main()