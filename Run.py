import json
with open("User_ip.json",'r') as file:
    user=json.load(file)

user_names=list(user.keys())


keys={
    1:"Never gonna give you up",
    2:"Never gonna let you down",
    3:"Never gonna turn around and hate you"
}



with open("Candidate_Block.json",'w') as f:
    json.dump(keys,f,indent=4)
