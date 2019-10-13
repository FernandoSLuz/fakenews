import sys
import os
import time
import json
import dialogflowBackend as dialogScript

import flask
from flask import Blueprint
from flask import request

blueprint = flask.Blueprint('wassengerBackend', __name__)


class user():
    id = 0
    phone = ""
    name = ""
    conversationid = ""

actualUser = user()



@blueprint.route('/webhook', methods=[ 'POST' ])
def webhook():
    print("test")
    form = request.get_json(silent=True, force=True)
    res = (json.dumps(form, indent=3))
    if(res is 'null'):
        return {'fulfillmentText': '404'}
    else:
        intentName = form['queryResult']['intent']['displayName']
        return {'fulfillmentText': "Intent " + intentName + " not listed on our database"}

def sendWassengerMessage(phoneNumber, message):
    import requests as req
    print("phone = " + phoneNumber + " ----- message = " + message)
    url = "https://api.wassenger.com/v1/messages"

    payload = "{\"phone\":\""+phoneNumber+"\",\"priority\":\"urgent\",\"message\":\""+ message +"\"}"

    #print("old payload = " + payload)
    headers = {
        'content-type': "application/json",
        'token': "905bd94b9d3a26df733849887c838b9cc5ee1538b72fb1937edf027d5b7b71c71b2c54f1c894e4a2"
        }

    res = req.request("POST", url, data=payload, headers=headers)
    res.json() if res.status_code == 200 else []
    print(res.content)
    return res.status_code
    #print(res.json())


@blueprint.route('/recieveWassengerMessage', methods=[ 'POST', 'GET' ])
def recievemessage():
    import bd
    from flask import request
    global actualUser
    newUser = user()
    form = request.get_json(silent=True, force=True)
    res = (json.dumps(form, indent=3))
    recievedMessage = ""
    recievedPhone = ""
    if(str(form['data']['chat']['contact']['type']) == 'user'):
        #print(form)
        recievedMessage = str(form['data']['body'])
        newUser.phone = str(form['data']['fromNumber'])
        newUser = bd.find_user(newUser,"users","phone",newUser.phone)
        if(newUser.conversationid == ""):
            print("user created")
            newUser = bd.insert_user(newUser, "users", "phone", newUser.phone)
        else:
            print("user found")
        #test = bd.select_all_users("users")
        #print("phone = " + newUser.phone)
        #print("conversationId = " + newUser.conversationid)
        #print("name = " + newUser.name)
        dialogCallBackMessage = dialogScript.checkNumberStatus(newUser, recievedMessage)
        sendWassengerMessage(newUser.phone, dialogCallBackMessage)
        #test####
        #sendWassengerMessage(recievedPhone, recievedMessage)
        return "200"
    else:
        return("---------------> message is not from user. Type = " + str(form['data']['chat']['contact']['type']))
