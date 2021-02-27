import time
import hash
import rsa

def cloneTable(t):
  newT = {}
  for k,v in t.items():
    newT[k] = v
  return newT

class State:
  def __init__(self,moneyDict,moneyStakedDict):
    self.moneyDict = moneyDict
    self.moneyStakedDict = moneyStakedDict

  def copy(self):
    return State(cloneTable(self.moneyDict),cloneTable(self.moneyStakedDict))
    
  def amtMoney(self,user):
    return self.moneyDict[user.getPublicKey()] or 0
  def amtStakedMoney(self,staker):
    return self.moneyStakedDict[staker.getPublicKey()] or 0

  def addSubMoney(self,person,amt,mutable=False):
    state = self.copy() if mutable else self
    if amt < 0:
      if state.amtMoney(person) < amt: # can't get negative balance
        return False

    state.moneyDict[person.getPublicKey()] = state.amtMoney(person) + amt # we don't use += because it could be None
    if state.moneyDict[person.getPublicKey()] == 0:
      del state.moneyDict[person.getPublicKey()]
    
    return state

  def addSubStakedMoney(self,staker,amt,mutable=False):
    state = self.copy() if mutable else self
    if amt < 0:
      if state.amtStakedMoney(staker) < amt: # can't get negative balance
        return False

    state.moneyStakedDict[staker.getPublicKey()] = state.amtStakedMoney(staker) + amt # we don't use += because it could be None
    if state.moneyStakedDict[staker.getPublicKey()] == 0:
      del state.moneyStakedDict[staker.getPublicKey()]
    
    return state

class Txn:
  def __init__(self,senders,sentAmts,receivers,receivedAmts,signatures):
    self.senders = senders
    self.sendAmts = sentAmts
    self.receivers = receivers
    self.receivedAmts = receivedAmts
    self.signatures = signatures

  def getHash(self):
    msg = b""
    msg += hash.hashList(self.senders)
    msg += hash.hashList(self.sentAmts)
    msg += hash.hashList(self.receivers)
    msg += hash.hashList(self.receivedAmts)
    msg += hash.hashList(self.signatures)
    return hash.ourHash(msg)

  def modifyState(self,state,mutable=False):
    if len(self.senders) != len(self.signatures):
      state = False
    else:
      sigsAreGood = True
      for i in range(len(self.senders)):
        sdr = self.senders[i]
        sig = self.signatures[i]
        sigsAreGood = sigsAreGood and sig.signer == sdr.getPublicKey()
        sigsAreGood = sigsAreGood and sig.validSignatureOf(self.getHash())
      if not sigsAreGood:
        state = False
    
    if len(self.senders) != len(self.sentAmts):
      return False

    sentAmt = 0
    for i in range(len(self.senders)):
      if state == False:
        return False
      sdr = self.senders[i]
      amt = self.sentAmts[i]
      sentAmt += amt
      state = state.addSubMoney(sdr,-amt)
    
    if len(self.receivers) != len(self.receivedAmts):
      return False

    receivedAmt = 0
    for i in range(len(self.reveivers)):
      if state == False:
        return False
      rcv = self.receivers[i]
      amt = self.receivedAmts[i]
      receivedAmt += amt
      state = state.addSubMoney(rcv,amt)
    
    return state
    


# TODO txn to put money up for staking

def currentTime(): #returns UNIX time in seconds
  time2 = int(time.time())
  return time2

def blockTime(difficulty,moneyContributed):
  # TODO might be completely wrong and bad
  if moneyContributed == 0:
    return 0
  else:
    return difficulty // moneyContributed

class Block:
  def __init__(self,txns,stakers,stakerSigs,timestamp,prevBlock):
    self.txns = txns
    self.stakers = stakers
    self.stakerSigs = stakerSigs
    self.timestamp = timestamp
    self.prevBlock = prevBlock

  def getPreSignatureHash(self):
    if not self.preSignatureHash:
      msg = b""
      msg += self.prevBlock.getHash()
      msg += hash.hashList(self.txns)
      self.preSigHash = hash.ourHash(msg)

    return self.preSignatureHash

  def getHash(self):
    if not self.hash:
      msg = b""
      msg += self.getPreSignatureHash
      msg += hash.hashList(self.stakers)
      msg += hash.hashList(self.stakerSigs)
      msg += hash.ourHash(self.timestamp)
      self.preSigHash = hash.ourHash(msg)

    return self.hash
    
  def getState(self):
    if self.state == None:
      state = self.prevBlock.getState()
      if state != False:
        state = state.copy()
      # btw False state just means like "bad invalid block, do not use"
      for txn in self.txns:
        state = txn.modifyState(state,True)

      moneyContributed = 0
      if not state or len(self.stakers) != len(self.stakerSigs):
        state = False
      else:
        alreadyContributed = {}
        for i in range(len(self.stakers)):
          stk = self.stakers[i]
          sig = self.stakerSigs[i]

          isGood = True
          isGood = isGood and sig.signer == stk.getPublicKey()
          isGood = isGood and sig.validSignatureOf(self.getPreSignatureHash())
          isGood = isGood and self.alreadyContributed[stk] == None

          alreadyContributed[stk] = True
          moneyContributed += state.amtStakedMoney(stk)

          if not isGood:
            state = False
            break

      if state and moneyContributed != 0:
        blockReward = 500 # TODO
        for s in self.stakers:
          state = state.addSubMoney(s,blockReward*state.amtStakedMoney(s)//moneyContributed,True)

      if self.timestamp < self.prevBlock.timestamp + blockTime(state.difficulty,moneyContributed):
        state = False

      self.state = state

    return self.state

class Stk():
  def __init__(self, publicKey):
    self.publicKey = publicKey
  def getPublicKey(self):
    return self.publicKey

#Sig in RSA
    
mmm = Txn([],[],[],[],[])
