from hashlib import sha512
'''
import hashlib
m = hashlib.sha512()
m.update(b"penis")
m.update(b"2")
m.digest()
m.digest_size
m.block_size

n = hashlib.sha512()
n.update(b"bob")
n.digest()
n.digest_size
n.block_size
'''

def ourHash(msg):
  return sha512(msg).digest()

def hashList(l):
  msg = b""
  msg += ourHash(len(l))
  for t in l:
    msg += t.getHash()
  return ourHash(msg)

#hexdigest() can be used to return values of digest as hex characters in a string

#dk = hashlib.pbkdf2_hmac('sha512', b'password', b'salty o my', 100000)
#hashlib.pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None)

#^not necessary but neat widepeepohappy