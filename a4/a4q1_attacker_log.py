import base64
import json
import random
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from sympy import mod_inverse
from sympy.ntheory import factorint, isprime

def bytes2string(b):
    return base64.urlsafe_b64encode(b).decode('utf-8')

def string2bytes(s):
    return base64.urlsafe_b64decode(s.encode('utf-8'))

def gen_rsa_pk():
    bitlength = 512
    p = random.randint(2 ** (bitlength - 1), 2 ** bitlength) # sketchy
    if not(isprime(p)): p = random.randint(2 ** (bitlength - 1), 2 ** bitlength) # what if it isn't prime?
    q = random.randint(2 ** (bitlength - 1), 2 ** bitlength) # sketchy
    if not(isprime(q)): q = random.randint(2 ** (bitlength - 1), 2 ** bitlength) # what if it isn't prime?
    n = p * q
    e = random.randint(2 ** 128, 2 ** 129 - 1) # sketchy
    return (n, e)

def gen_prime(bitlength):
    return randprime(2 ** (bitlength-1), 2 ** bitlength) # sketchy

def do_encryption():
    # read the assignment file to be encrypted
    with open("assignment_in.pdf", 'rb') as fh:
        plaintext = fh.read()

    # generate the RSA public key
    (n, e) = gen_rsa_pk()

    # generate an AES key and convert it to an integer
    aes_key = random.randbytes(16)
    aes_key_int = int.from_bytes(aes_key, byteorder='big')
    
    # encrypt the AES key using RSA encryption
    c_1 = pow(aes_key_int, e, n)

    # pad the plaintext to a multiple of the block length
    padder = padding.PKCS7(128).padder() # 128 is the block size
    padded_data = padder.update(plaintext)
    padded_data += padder.finalize()
    
    # encrypt the plaintext using AES
    cipher = Cipher(algorithms.AES(aes_key), modes.ECB()).encryptor()
    aes_ct = cipher.update(padded_data) + cipher.finalize()

    # output the data in a JSON data structure for easy parsing
    output = {}
    output["n"] = n
    output["e"] = e
    output["c_1"] = c_1
    output["c_2"] = bytes2string(aes_ct)
    with open("encrypted_assignment.json.txt", 'w') as fh:
        fh.write(json.dumps(output))

def do_decryption():
    
    # Read and parse the JSON data structure
    with open("encrypted_assignment.json.txt", 'r') as fh:
        input = json.loads(fh.read())
    n = input["n"]
    e = input["e"]
    c_1 = input["c_1"]
    c_2 = string2bytes(input["c_2"])

    factored_n = factorint(n)
    factors = list(factored_n.keys())
    phi = 1
    for i in range(0, len(factors)):
        phi = phi * (factors[i] - 1)
        
    try:
        d = mod_inverse(e, phi)
    except:
        print("NO")

    key = pow(c_1, d, n)

    print(key)
    key = key.to_bytes(16, byteorder='big') # why does this cause error
    
    cipher = Cipher(algorithms.AES(key), modes.ECB()).decryptor()

    plaintext = cipher.update(c_2) + cipher.finalize()

    padder = padding.PKCS7(128).unpadder() # 128 is the block size
    plaintext = padder.update(plaintext)
    plaintext += padder.finalize()

    # write the decrypted assignment to a file
    with open("assignment_out.pdf", 'wb') as fh:
        fh.write(plaintext)

do_decryption()
