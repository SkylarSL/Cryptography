from datetime import datetime
import json
import sys
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from cryptography.hazmat.primitives import serialization

# Helper function for converting strings into byte arrays needed by cryptographic functions
def string_to_bytes(s):
    return s.encode('utf-8')

# This function will ensure that we represent the JSON dictionary as exactly the
# same string every time, otherwise we'd get different hashes while signing
def canonicalize_json(j):
    return json.dumps(j, sort_keys=True)

# Parse the command-line arguments
if len(sys.argv) != 3:
    print('Usage: verify_soln.py ca_identity message.signed.txt')
ca_identity = sys.argv[1]
signed_message_filename = sys.argv[2]

# Load the signed message data
with open(signed_message_filename, 'r') as fh:
    signed_message = json.load(fh)

# Read out the identity of the signer and load their certificate
signer_identity = signed_message['signer identity']
with open(signer_identity + '.cert', 'r') as fh:
    signer_cert = json.load(fh)
# Format the certificate body for signing as a byte array in a canonical order
cert_body_to_be_signed = string_to_bytes(canonicalize_json(signer_cert["body"]))

# Read out the identity of the issuer and load their public key
issuer_identity = signer_cert['body']['issuer identity']
signer_pk = serialization.load_pem_public_key(string_to_bytes(signer_cert['body']['public key']))
with open(ca_identity + '.pk', 'r') as fh:
    ca_public_key = serialization.load_pem_public_key(string_to_bytes(fh.read()))

# YOUR SOLUTION STARTS HERE

# a) 
# Check that 0 < r < q, 0 < s < q, and since this was signed using ECDSA we 
# need to check that the x value of ((H(m)/s)P)+((r/s)(alpha)P) is congruent to r mod q. 
# Additionally, you should check the validity of the certificate that signed the messege. 
# You could check expiry date, issuer identity, etc.

# b)

# check that the certs issuer is the CA cert 
if(json.loads(cert_body_to_be_signed.decode("utf-8"))["issuer identity"] != issuer_identity):
    print("not valid")

print(signer_cert, "\n")

message = bytes(signed_message["message"], "utf-8")
r = signer_cert["signature"]["r"]
s = signer_cert["signature"]["s"]
signing = encode_dss_signature(r, s)

print(cert_body_to_be_signed, "\n")

try:
    ca_public_key.verify(signing, cert_body_to_be_signed, ec.ECDSA(hashes.SHA256()))
    print("valid")
except:
    print("not valid")

message = bytes(signed_message["message"], "utf-8")
r = signed_message["signature"]["r"]
s = signed_message["signature"]["s"]
signing = encode_dss_signature(r, s)
try:
    signer_pk.verify(signing, message, ec.ECDSA(hashes.SHA256()))
    print("valid")
except:
    print("not valid")

# checked manually
validend = datetime.fromisoformat(json.loads(cert_body_to_be_signed.decode("utf-8"))["validity end"])
validstart = datetime.fromisoformat(json.loads(cert_body_to_be_signed.decode("utf-8"))["validity start"])
print("atart: ", validstart, "end: ", validend)

# c) 
# messege1 is legitamate. 
# messege2 does not verify when checking the signing of the message.
# messege3 does not verify when checking the signing of the certificate that is used to sign the message.
# messege4 is signed by a cert that is not signed by the CA. It is a self signed certificate and should not be trusted.
# messege5 is signed by an expired cert.

# Functions that might be of use to you:
# - datetime.fromisoformat (https://docs.python.org/3/library/datetime.html#datetime.date.fromisoformat)
# - encode_dss_signature (https://cryptography.io/en/latest/hazmat/primitives/asymmetric/utils/#cryptography.hazmat.primitives.asymmetric.utils.encode_dss_signature)
# - ca_public_key.verify and signer_pk.verify (see https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/#elliptic-curve-signature-algorithms)
