import sys, os
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import utility

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'MT19937-password-reset'))
from MT19937 import MT19937

SITE_URL  = "http://localhost:8080"

USERNAME = "hayk"
PASSWORD = "123456"
NEW_ADMIN_PASS = "hacked123"

# MT19937 tempering constants
B = 0x9D2C5680
C = 0xEFC60000


# Undo the temper in reverse order
def undoTemper(z):

    # undo: y ^= (y >> l)  where l = 18
    # Recover bits top-down: each pass recovers another 18 bits
    y = z
    for _ in range(32 // 18 + 1):
        y = z ^ (y >> 18)
    y = y & 0xFFFFFFFF

    # undo: y ^= (y << t) & c  where t = 15, c = C
    # Recover bits bottom-up: each pass recovers another 15 bits
    x = y
    for _ in range(32 // 15 + 1):
        x = y ^ ((x << 15) & C)
    x = x & 0xFFFFFFFF

    # undo: y ^= (y << s) & b  where s = 7, b = B
    # Recover bits bottom-up: each pass recovers another 7 bits
    w = x
    for _ in range(32 // 7 + 1):
        w = x ^ ((w << 7) & B)
    w = w & 0xFFFFFFFF

    # undo: y ^= (y >> u)  where u = 11
    # Recover bits top-down: each pass recovers another 11 bits
    v = w
    for _ in range(32 // 11 + 1):
        v = w ^ (v >> 11)
    v = v & 0xFFFFFFFF

    return v


# Send a password reset request and return the server response
def sendRequest(session, username):
    return session.post(SITE_URL + "/forgot", data={"user": username})


# Extract the base64 token from the response and decode it into 8 MT outputs
def parseToken(response):

    # Bounds check
    start = response.text.find('<!--open_token-->')
    end   = response.text.find('<!--close_token-->')
    if start == -1 or end == -1:
        return None

    content = response.text[start + len('<!--open_token-->'):end].strip()
    idx = content.find('?token=')
    if idx == -1:
        return None

    token = content[idx + len('?token='):]
    return [int(x) for x in utility.base64ToByte(token).decode().split(':')]


def task2():
    session = requests.Session()

    # Register a test account to collect tokens from
    session.post(SITE_URL + "/register", data={"user": USERNAME, "password": PASSWORD})

    # Collect 78 tokens
    print("Sending 78 password requests!")
    observed = []
    for i in range(78):
        response = sendRequest(session, USERNAME)
        token = parseToken(response)

        if not token:
            return

        observed.extend(token)

    # Unmix each output
    print("Undoing temper")
    mtState = [undoTemper(v) for v in observed]
    print("Recovered " + str(len(mtState)) + " values")

    # Initialize MT19937
    clone = MT19937(b'0')
    
    # Set 
    clone.mt = mtState[:]
    clone.index = 624

    # Predict the next 8 outputs from MT19937
    # ^ the server generates 256 bit random number
    # 8 * 32 bits = 256 <-------
    outputs = [str(clone.extract_number()) for i in range(8)]

    # Join the outputs and base64 encode
    data = ":".join(outputs)
    predictedToken = utility.byteToString(utility.stringToBase64(data))

    print("Admin token: " + predictedToken)

    # Trigger the admin reset on the server
    session.post(SITE_URL + "/forgot", data={"user": "admin"})

    # http://localhost:8080/reset?token="predictedtoken"



if __name__ == "__main__":
    task2()
