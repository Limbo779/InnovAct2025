import hashlib as hs
import pickle

block={
    "timestamp":"2025-08-25,3:37am",
    "sender_key":"1235996",
    "receiver_key":"7894456",
    "prev_hash":"84bac90df",
    "msg":"dcnkjn121cnjs",
    "sign":"cb89cd9af",
    "nonce":-1
}

a=0.9998203319067136
target=26502705971675764943749462511143777737412258453134284371824093019389296640
new_target=round(target*(a**(10000)))

while True:
    hasher=hs.new('sha256')
    block['nonce']+=1
    print(block['nonce'])
    block_bytes=pickle.dumps(block)
    hasher.update(block_bytes)
    hash=hasher.hexdigest()
    if int(hash,16) < new_target :
        break
    else:
        continue

print(hash)