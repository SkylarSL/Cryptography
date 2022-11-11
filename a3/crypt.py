import os
import sys
import getpass
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64decode, urlsafe_b64encode

def AESecrypt(key, message: bytes):
    # AES128 with CBC
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES128(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(message) + encryptor.finalize()
    return (ct, iv)

def AESdecrypt(key, iv, message):
    # AES128 with CBC
    cipher = Cipher(algorithms.AES128(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    pt = decryptor.update(message) + decryptor.finalize()
    return pt
    
def pad(message: bytes):
    # PKCS7 padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message)
    padded_data += padder.finalize()
    return padded_data

def unpad(message: bytes):
    # unpad
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(message)
    print(data)
    data = data + unpadder.finalize()
    return data

def HMAChash(key, message):
    # HMAC hashing
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(message)
    signature = h.finalize()
    return signature
    
def verifyhash(key, signature, message):
    # verify
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(message)
    h_copy = h.copy() # get a copy of `h' to be reused
    try:
        h_copy.verify(signature)
        print("GOOD")
    except:
        print("BAD")
        return -1
    return 0
    

def derivekey(password: bytes):
    # PBKDF2 key derivation
    # Salts should be randomly generated
    salt = os.urandom(16)
    # derive
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=16,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password)
    return key

def encrypt():
    password = getpass.getpass()
    password2 = getpass.getpass("Enter password again:")

    if password != password2:
        sys.stderr.write("Passwords did not match")
        sys.exit()

    # grab input
    text = sys.argv[2]
    text = bytes(text, "utf-8")
    password = bytes(password, "utf-8")
    # derive the key
    key = derivekey(password)
    # pad the text to fit size
    paddedpt = pad(text)
    # enrypt and get iv and cipher
    ct, iv = AESecrypt(key, paddedpt)
    # make the message
    message = iv + ct
    # hash the message
    signature = HMAChash(key, message)
    # send the encoded signature and message
    final = urlsafe_b64encode(signature + message)

    print(final)


def decrypt():
    password = getpass.getpass()
    password2 = getpass.getpass("Enter password again:")

    if password != password2:
        sys.stderr.write("Passwords did not match")
        sys.exit()
    password = bytes(password, "utf-8")

    # grab inputs
    text = sys.argv[2]
    text = urlsafe_b64decode(text)
    hash, text = text[0:32], text[32:]
    # derive the key
    key = derivekey(password)
    # check if the hash verifies
    if verifyhash(key, hash, text) == -1:
        print("bad hash")
        exit()
    # get the iv and cipher
    iv, ct = text[0:16], text[16:]
    # decode the cipher
    pt = AESdecrypt(key, iv, ct)
    # unpad it
    pt = unpad(pt)
    print(pt.decode("utf-8"))

try:
    mode = sys.argv[1]
    assert( mode in ['-e', '-d'] )
except:
    sys.stderr.write("Unrecognized mode. Usage:\n")
    sys.stderr.write("py crypt.py -e <message\n")
    sys.stderr.write("py crypt.py -d <message'\n")

if mode == '-e':
    encrypt()
elif mode == '-d':
    decrypt()