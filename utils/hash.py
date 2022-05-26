import hashlib

def hash_pass(password):
    str = password.encode('utf-8')
    hex_str = str.hex()
    return hex_str

def dehash_pass(hash_pass):
    password = hash_pass.decode('hex') 
    return password

