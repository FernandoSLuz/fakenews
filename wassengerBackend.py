import sys
import os
import time
import json
import dialogflowBackend as dialogScript
import re

import flask
from flask import Blueprint
from flask import request

blueprint = flask.Blueprint('wassengerBackend', __name__)


class user():
    id = 0
    phone = ""
    name = ""
    conversationid = ""

class news():
    id = 0
    url = ""
    userid = 0

class vote():
    id = 0
    urlid = 0
    userid = 0
    votetype = 0




@blueprint.route('/dialogwebhook', methods=[ 'POST' ])
def dialogwebhook():
    import bd
    form = request.get_json(silent=True, force=True)
    #res = (json.dumps(form, indent=3))
    actualUser = user()
    actualUser.conversationId = re.sub(r"\W", "", str(form['session']).rsplit('/',1)[1])
    
    #print("big = " + actualUser.conversationId )

    actualUser = bd.find_user(actualUser, "users", "conversationid", actualUser.conversationId)
    print("USER CONVERSATION ID = " + actualUser.conversationid)
    intentName = str(form['queryResult']['intent']['displayName'])
    if(intentName == "envio_do_link" or intentName == "link_direto"):
        actualNews = news()
        #actualNews.userid = actualUser.id
        actualNews.url = str(form['queryResult']['outputContexts'][0]['parameters']['url'])
        actualNews = bd.find_news(actualNews, "news", "url", actualNews.url)
        print("id = " + str(actualNews.id))
        if(actualNews.userid == 0):
            actualNews.userid = actualUser.id
            actualNews = bd.insert_news(actualNews, "news", "url", actualNews.url)
            return "Obrigado, o link foi recebido e está sendo analizado!"
        votes = bd.find_votes("votes", "urlid", actualNews.id)
        if(votes[0] == 0 and votes[1] == 0 and votes[2] == 0): return "Obrigado, o link foi recebido e está sendo analizado!"
        true = "Pessoas que acreditam que a notícia é verdadeira: " + str(votes[0])
        unknown = "Pessoas que acreditam que a notícia é parcialmente verdadeira: " + str(votes[1])
        fake = "Pessoas que acreditam que a notícia é falsa: " + str(votes[2])

        message = "Notícia: " + str(actualNews.id) + " ---- " + true + unknown + fake
        content = {
            'message': message
        }
        return content
    return "não achei o link, malz ae"
    
    #if()

def sendWassengerMessage(phoneNumber, message):
    import requests as req
    #print("phone = " + phoneNumber + " ----- message = " + message)
    url = "https://api.wassenger.com/v1/messages"

    payload = "{\"phone\":\""+phoneNumber+"\",\"priority\":\"urgent\",\"message\":\""+ message +"\"}"

    #print("old payload = " + payload)
    headers = {
        'content-type': "application/json",
        'token': "905bd94b9d3a26df733849887c838b9cc5ee1538b72fb1937edf027d5b7b71c71b2c54f1c894e4a2"
        }

    res = req.request("POST", url, data=payload, headers=headers)
    res.json() if res.status_code == 200 else []
    #print(res.content)
    return res.status_code
    #print(res.json())


@blueprint.route('/recieveWassengerMessage', methods=[ 'POST', 'GET' ])
def recievemessage():
    import bd
    from flask import request
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
