import hashlib


def hash_pass(password):
    str = password.encode('utf-8')
    hash_pass = str.hex()
    return hash_pass

def dehash_pass(hash_pass):
    password = hash_pass.decode('hex') 
    return password