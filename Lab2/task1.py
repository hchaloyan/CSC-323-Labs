import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import utility

# 16 Bytes
blockSize = 16


def pad(plaintext: bytes, blockSize: int = blockSize) -> bytes:
    
    # blockSize must fit in a single byte
    if blockSize < 1 or blockSize > 255:
        print("Block size invalid!")
        sys.exit(1)

    padLength = blockSize - (len(plaintext) % blockSize)




    # Each padding byte holds the count of padding bytes added
    # Got from RFC 5652 Section 6.3
    return plaintext + bytes([padLength] * padLength)


def unpad(padded: bytes, blockSize: int = blockSize) -> bytes:
    
    # Error if empty
    if not padded:
        print("EMPTY!")
        return

    # Padded must be a whole number of blocks
    if len(padded) % blockSize != 0:
        print("Not a whole number of blocks")
        return

    # The last byte = amount of bytes padded
    padLength = padded[-1]

    # padLength must be at least 1 and at most one full block
    if padLength < 1 or padLength > blockSize:
        print("Invalid pad length")
        return

    padding = padded[-padLength:]

    # Every padding byte must equal padLength
    if any(byte != padLength for byte in padding):
        print("Padding byte not equal to pad length!!")
        return

    return padded[:-padLength]


def task1():
    
    msg = b"HELLOO WORLDD"
    padded = pad(msg)
    
    print(msg)
    print(padded)
    print(unpad(padded))


if __name__ == "__main__":
    task1()
