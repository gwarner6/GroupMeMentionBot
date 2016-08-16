import requests
import re
import json




token="INSERT YOUR ACCESS TOKEN FROM GROUP ME"

botid="INSERT YOUR BOT ID FROM GROUP ME HERE"

BASE_URL="https://api.groupme.com/v3"

params={'bot_id':botid,'token':token}


#HARD CODED LIST OF USER IDS of users in GroupME group who are considered Moderators
mod_ids=[]


#fetches and maps the ids to the users in mod_id to their chat names
#returns a dictionary
def getModNickNames():
    r=requests.get("https://api.groupme.com/v3/groups/9829189?token=4cfcf710421c0134d0fe41117ad5492d")
    json_response=r.json()
    user_dict=json_response[u'response'][u'members']


    mod_dic={}

    for user in user_dict:

        if(str(user[u'user_id']) in mod_ids ):

            nickname="@"+user[u'nickname']
            mod_dic[str(user[u'user_id'])]=str(nickname)


    return mod_dic

#Builds the string that will be included in the json "text" field
#returns a string
def makeString():

    mods=getModNickNames();
    ret=""
    for value in mods.itervalues():
        ret+=value


    return ret


#Builds the list need by group me mention attachment types 
#returns a list
def buildLociList(ModString):

    list=[]

    for m in re.finditer('@',ModString):
        userloci=[m.start()]
        list.append(userloci)


    
    count=0;
    for name in ModString.split("@"):
        if name.__len__()!=0:
            list[count].append(name.__len__()+1)
            count=count +1
            # print name;


    return list

#Builds and Sends Json using groupme bot API
def sendJson():
    textstring=makeString()

    l=buildLociList(textstring)

    id=getModNickNames()


    mod_ids=[]
    for key in id.iterkeys():

        mod_ids.append(key)
    

    json_string={}

    attachments={}


    json_string["bot_id"]=botid
    json_string["text"]=textstring

    attachments['user_ids']=mod_ids

    attachments['loci']=l
    attachments['type']="mentions"

    attachment=[attachments]

    json_string['attachments']=attachment


    r=requests.post("https://api.groupme.com/v3/bots/post",data=json.dumps(json_string),params=params)
    