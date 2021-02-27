from Crypto.PublicKey import RSA
#from Crypto.Cipher import PKCS1_OAEP
from hashlib import sha512

class personalKey:
  def __init__(self, encrypted_key = None, passphrase = None):
    if personalKey != None:
      try:
        self.keyPair = RSA.import_key(encrypted_key, passphrase)
      except:
        print("what are you regarded")
    else:
      self.keyPair = RSA.generate(4096)
  
  def sign(self, msg):
    hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
    return pow(hash, self.keyPair.d, self.keyPair.n)
  
  def getPublicKey(self):
    return (self.keyPair.n, self.keyPair.e)
  
  def getWholeKey(self, passphrase):
    encrypted_key = self.keyPair.export_key(passphrase, pkcs=8, protection="scryptAndAES128-CBC")
    return encrypted_key
  
  def signHash(self, hash):
    return Sig(self.getPublicKey(), self.sign(hash))

class Sig():
  def __init__(self, publicKey, signature):
    self.signer = publicKey
    self.signature = signature
    #everyone is denoted by their public key, a tuple of (n, e)
  def validSignatureOf(self, hash):
    hashFromSignature = pow(self.signature, self.publicKey[1], self.publicKey[0])
    return hashFromSignature == hash

'''
#hash = int.from_bytes(sha512(msg).digest(), byteorder='big')

keyPair = RSA.generate(3072)

pubKey = keyPair.publickey()
#print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
pubKeyPEM = pubKey.exportKey()
#print(pubKeyPEM.decode('ascii'))

#print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")
privKeyPEM = keyPair.exportKey()
#print(privKeyPEM.decode('ascii'))

msg = b'Try me bitch'
encryptor = PKCS1_OAEP.new(pubKey)
encrypted = encryptor.encrypt(msg)
#print("Encrypted:", binascii.hexlify(encrypted))

decryptor = PKCS1_OAEP.new(keyPair)
decrypted = decryptor.decrypt(encrypted)
#print('Decrypted:', decrypted)

msg = b'im feeling so signed rn'
hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
signature = pow(hash, keyPair.d, keyPair.n)
#print("Signature:", hex(signature))

hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
hashFromSignature = pow(signature, keyPair.e, keyPair.n)
print("Signature valid:", hash == hashFromSignature)
'''