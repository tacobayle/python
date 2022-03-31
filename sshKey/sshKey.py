from os import chmod
from Crypto.PublicKey import RSA

key = RSA.generate(2048)
with open("/home/nic/private.key", 'wb') as content_file:
    chmod("/home/nic/private.key", 0o600)
    content_file.write(key.exportKey('PEM'))
pubkey = key.publickey()
with open("/home/nic/public.key", 'wb') as content_file:
    content_file.write(pubkey.exportKey('OpenSSH'))
