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
    newsid = 0

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
    actualUser = user()
    actualUser.conversationId = re.sub(r"\W", "", str(form['session']).rsplit('/',1)[1])
    actualUser = bd.find_user(actualUser, "users", "conversationid", actualUser.conversationId)
    intentName = str(form['queryResult']['intent']['displayName'])
    if(intentName == "envio_do_link" or intentName == "link_direto"):
        actualNews = news()
        actualNews.url = str(form['queryResult']['outputContexts'][0]['parameters']['url'])
        actualNews = bd.find_news(actualNews, "news", "url", actualNews.url)
        if(actualNews.userid == 0):
            actualNews.userid = actualUser.id
            actualNews = bd.insert_news(actualNews, "news", "url", actualNews.url)
            content = {
                'message': "Obrigado, o link foi recebido e será analisado!"
            }
            return content
        votes = bd.find_votes("votes", "urlid", actualNews.id)
        #CHANGE LATER
        if(votes[0] == 0 and votes[1] == 0 and votes[2] == 0): 
            content = {
                'message': "Obrigado, o link foi recebido e está sendo analisado!"
            }
            return content
        true = "Pessoas que acreditam que a notícia é verdadeira: " + str(votes[0])
        unknown = "Pessoas que acreditam que a notícia é parcialmente verdadeira: " + str(votes[1])
        #unknown = "\\2B1B"  

        fake = "Pessoas que acreditam que a notícia é falsa: " + str(votes[2])

        termometro = MontarTextoTermometro((votes[0]+1),(votes[2]+1))

        message = "Notícia: " + str(actualNews.url) + "\\n\\n" + true + "\\n\\n" + unknown + "\\n\\n" + fake  + "\\n\\n" + termometro

        content = {
            'message': message
        }
        return content
    if(intentName == "escolheu_analisar"):
        actualNews = news()
        actualNews = bd.look_for_user_votes("news", actualNews, actualUser)

        if(actualNews.url == ""):
            content = {
                'message': "Que bom! Você já averiguou todas as notícias até o momento!"
            }
            return content
        else:
            content = {
                'message': "Temos uma notícia para você averiguar:\\n\\n" + actualNews.url + "\\n\\nAgora preciso que você digite:\\n\\n" + "'1' se considerar que é uma notícia verdadeira\\n'2' para uma notícia mentirosa ou\\n'3' se você não sabe se é uma noticia verdadeira."
            }
            return content
        content = {
            'message': "ERRO DE ANALISE"
        }
        return content
    if(intentName == "resultado_da_analise"):
        answer = str(form['queryResult']['outputContexts'][0]['parameters']['Opiniao_Veracidade'])
        answerid = -1
        introductionText = ""
        if(answer == "verdade"):
            introductionText = "Você selecionou a notícia como VERDADEIRA,"
            answerid = 0
        elif(answer == "falso"):
            introductionText = "Você selecionou a notícia como FALSA,"
            answerid = 2
        else: 
            introductionText = "Você selecionou a notícia como INCERTA,"
            answerid = 1
        
        print(form)
        actualNews = news()
        actualUser = bd.find_user(actualUser, "users", "conversationid", actualUser.conversationId)
        print("newsId - " + str(actualUser.newsid))
        print("userId - " + str(actualUser.id))
        print("conversationId - " + str(actualUser.conversationid))
        actualNews = bd.find_news_by_id(actualNews, "news", "id", actualUser.newsid)
        bd.insert_vote(actualNews, actualUser, answerid, "votes")
        votes = bd.find_votes("votes", "urlid", actualNews.id)
        true = "Pessoas que acreditam que a notícia é verdadeira: " + str(votes[0])
        unknown = "Pessoas que acreditam que a notícia é parcialmente verdadeira: " + str(votes[1])
        fake = "Pessoas que acreditam que a notícia é falsa: " + str(votes[2])

        message = introductionText + " Obrigado pela sua contribuição!\\n\\nSeguem estatísticas gerais desta notícia:" + "\\n\\n" + true + "\\n\\n" + unknown + "\\n\\n" + fake
        content = {
            'message': message
        }
        return content
    content = {
        'message': "ERRO DE INDENT, NENHUMA CONVERSA ENCONTRADA"
    }
    return content
    #incerto
    #falso
    #verdade
    
    #if()

def sendWassengerMessage(phoneNumber, message):
    import requests as req
    #print("phone = " + phoneNumber + " ----- message = " + message)
    url = "https://api.wassenger.com/v1/messages"

    payload = "{\"phone\":\""+phoneNumber+"\",\"priority\":\"urgent\",\"message\":\""+ message +"\"}"

    newbytes = payload.encode('utf-8')
    string = newbytes  #.decode('ASCII')

    print(payload)
    #print("old payload = " + payload)
    headers = {
        'content-type': "application/json",
        'token': "905bd94b9d3a26df733849887c838b9cc5ee1538b72fb1937edf027d5b7b71c71b2c54f1c894e4a2"
        }

    res = req.request("POST", url, data=string, headers=headers)
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




def MontarTextoTermometro(numTru, numFake):
	text = "Verdade "

	blackCode = "\U00002B1B" #"\2B1B";
	whiteCode = "\U0002b1c0" #"\2B1C";
	
	numTermo = numTru / (numTru + numFake) * 10

	for i in range(10):
	
		if i<numTermo:
			text += blackCode
		else:
			text += whiteCode

	text += " Fake"
	return text