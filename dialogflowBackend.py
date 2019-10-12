import sys
import os
import time
import json

import flask

from flask import Blueprint
import dialogflow
from google.protobuf import struct_pb2



blueprint = flask.Blueprint('dialogflowBackend', __name__)


def checkNumberStatus(newUser, newMessage):
    #AQUI CRIAREMOS UMA CONVERSA NOVA
    try:
        dialogCallBackMessage =  detect_intent_texts("lighthouse-vms", newUser.conversationid, newMessage, "pt-BR", newUser.phone)
        return dialogCallBackMessage
    except Exception as e:
        print(str(e))
        return ""

def detect_intent_texts(project_id, session_id, text, language_code, phone):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    import dialogflow_v2 as dialogflow2
    session_client = dialogflow2.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow2.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow2.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    #print('=' * 20)
    #print('Query text: {}'.format(response.query_result.query_text))
    #print('Detected intent: {} (confidence: {})\n'.format(
    #    response.query_result.intent.display_name,
    #    response.query_result.intent_detection_confidence))
    #print('Fulfillment text: {}\n'.format(
    #    response.query_result.fulfillment_text))
    
    return str(response.query_result.fulfillment_text)