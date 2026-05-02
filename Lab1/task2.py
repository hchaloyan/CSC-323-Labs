import sys, os
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import utility

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'MT19937-password-reset'))
from MT19937 import MT19937

SITE_URL  = "http://localhost:8080"

USERNAME = "hayk"
PASSWORD = "123456"

# MT19937 tempering constants
b = 0x9D2C5680
c = 0xEFC60000
l = 18
t = 15
s = 7
u = 11

# Undo the temper in reverse order, masking after each step
# Used this source to help understand:
    # https://occasionallycogent.com/inverting_the_mersenne_temper/index.html
    
def undoTemper(z):


    # undo: y ^= (y >> l)
    y = z
    for i in range(32 // l + 1):
        y = z ^ (y >> 18)
    
    y = y & 0xFFFFFFFF

    # undo: y ^= (y << t) & c
    x = y
    for i in range(32 // 15 + 1):
        x = y ^ ((x << 15) & c)
    
    x = x & 0xFFFFFFFF

    # undo: y ^= (y << s) & b
    w = x
    for i in range(32 // s + 1):
        w = x ^ ((w << s) & b)
    
    w = w & 0xFFFFFFFF

    # undo: y ^= (y >> u)
    v = w
    for i in range(32 // 11 + 1):
        v = w ^ (v >> 11)
    v = v & 0xFFFFFFFF


    return v


# Send a password reset request and return the server response
def sendRequest(session, username):
    return session.post(SITE_URL + "/forgot", data={"user": username})


# Decodes base64 token to 8 MT19937 outputs
def decodeToken(response):

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
    list = []
    for i in range(78):
        response = sendRequest(session, USERNAME)
        token = decodeToken(response)

        if not token:
            return

        list.extend(token)

    # Unmix each output
    print("Undoing temper")
    mtState = [undoTemper(v) for v in list]
    print("Recovered " + str(len(mtState)) + " values")

    # Initialize MT19937
    clone = MT19937(b'0')
    
    # Set 
    clone.mt = mtState[:]
    clone.index = 624

    # Predict the next 8 outputs from MT19937
        # the server generates 256 bit random number
        # 8 * 32 bits = 256
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
