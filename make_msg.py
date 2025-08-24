import rsa
import json
import pickle 
import base64
from datetime import datetime, timezone
import hashlib as hs
import os
import subprocess

def signature(x):
    with open('sk.pem','rb') as file:
        privkey=rsa.PrivateKey.load_pkcs1(file.read())
    s=rsa.sign(x, privkey, 'SHA-1')
    s=base64.b64encode(s)
    return s

def previous_hash(x):
    with open("Candidate_Block.json",'r') as file:
        Block=json.load(file)
    l=len(Block.keys())
    hasher=hs.new('sha256')
    content=pickle.dumps(Block[l])
    hasher.update(content)
    return hasher.hexdigest()

def Key_encode(x):
    binary=pickle.dumps(x)
    B64=base64.b64encode(binary)
    return B64.decode('utf-8')

def Key_decode(x):
    x=base64.b64decode(x)
    x=pickle.loads(x)
    return x

msg={}
# the components of the msg will added one by one

# getting the user's public key details
with open("User_key.json",'r') as file:
    User=json.load(file)

# choosing the user and their public key
user_choice=input("Enter the username : ")
receiver_key=Key_decode(User[user_choice][0])

# getting the public key of myself
with open('pk.pem','rb') as file:
    sender_key=rsa.PublicKey.load_pkcs1(file.read())

# timestamp and convo no
time=str(datetime.now(timezone.utc))
convo_no=User[user_choice][1]

# previous hash
prev_hash=previous_hash

# getting the actual message then encrypting it and storing it in the my_msg_log.json
message=input("Enter your message : ")

with open('my_msg_log.json','r') as file:    # This is to update the my_msg_log
    log=json.load(file)                      #
log[user_choice] += [message]                #
with open('my_msg_log.json','w') as file:    #
    json.dump(log,file,indent=4)             #


message=message.encode('utf-8')
message=rsa.encrypt(message,receiver_key)
l=[time,convo_no,sender_key,receiver_key,message]
l_bytes=pickle.dumps(l)
l.append(signature(l_bytes))
print(l)

sending_byte={
    time:l
}

with open('send_file.dat','wb') as file:
    pickle.dump(sending_byte,file)

with open('User_ip.json','r') as file:
    ip_log=json.load(file)

inputs = [ip_log[user_choice], 'send_file.dat']  
inputs_joined = '\n'.join(inputs) + '\n'

# Run the script with provided inputs
process = subprocess.Popen(['python', 'sending.py'],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           text=True)
stdout, stderr = process.communicate(input=inputs_joined)

# Print the output
print('Script Output:')
print(stdout.strip())
if stderr:
    print('Errors:')
    print(stderr.strip())

if stdout.strip()=='File sent successfully.':
    exit_code = os.system('rm -rf send_file.dat')
    













#with open("User_ip.json",'r') as file:
#    user=json.load(file)
#
#user_names=list(user.keys())
#
#
#keys={}
#for i in user_names:
#    pk,sk=rsa.newkeys(512)
#    binary=pickle.dumps(pk) # converting the key format to binary
#    B64=base64.b64encode(binary) # encode the binary to base64
#    k=(B64).decode('utf-8') # finally make base64 format to json string format
#    l=[k,0]
#    keys[i]=l
#
#
#with open("User_key.json",'w') as f:
#    json.dump(keys,f,indent=4)



