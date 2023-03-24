import datetime
import json

import requests

from botData.models.model_entities import Entity
from teams.models import ConversationParameters


def rasa_detect_intent(received_msg, conversation_id, bot_id):
    print('rasa hit')
    try:
        rasa_payload = {'text': received_msg,
                        'message_id': conversation_id}
        rasa_payload = json.dumps(rasa_payload)
        nlp_agent = bot_id.nlp_agent
        print('nlp_agent_123',nlp_agent.config['rasa_webhook'],rasa_payload)
        intent_res = requests.post(
            url='{}/model/parse?emulation_mode=dialogflow'.format(nlp_agent.config['rasa_webhook']),
            data=rasa_payload)
        print('ressssss',intent_res.text)
        intent_res = json.loads(intent_res.text)
        df_intent = intent_res['queryResult']['intent']['displayName']
        df_parameters = intent_res['queryResult']['parameters']
        context = None
        if intent_res['queryResult']['outputContexts']:
            output_context = intent_res['queryResult']['outputContexts']
            list_key = []
            for i in output_context:
                key_len = len(i.parameters.keys())
                list_key.append(key_len)
            max_key = list_key.index(max(list_key))
            context = output_context[max_key].parameters
        parameters = context if context is not None else df_parameters
        print('rasa parameters',parameters)
        if not parameters == {}:
            parameters = check_parameters(conversation_id=conversation_id, parameters=parameters, bot_id=bot_id)
            print('rasa detect-param',parameters)
        print('rasa detect-param-12234',df_intent)
        if df_intent == 'welcome':
            if ConversationParameters.objects.filter(conversation_id=conversation_id).first():
                conv_obj = ConversationParameters.objects.filter(conversation_id=conversation_id).first()
                conv_obj.parameters = reset_parameters_list(bot_id)
                conv_obj.save()
        res = {"intent_res": intent_res, "parameters": parameters}
        return res

    except Exception as e:
        print('rasa exception', e)


def reset_parameters_list(bot_id):
    # params = {
    #     "action": "",
    #     "component": "",
    #     "category": "",
    #     "subcategory": "",
    #     "summary": "",
    #     "description": "",
    #     "reason": "",
    #     "confirmation": "",
    #     "extension_location": "",
    #     "ticketStatus": "",
    #     "time_period": "",
    #     "operations": "",
    #     "any": "",
    #     "option": "",
    #     "media": "",
    #     "hostenable": "",
    #     "actionenable": "",
    #     "web": "",
    #     "hostgroup": "",
    #     "opportunity": "",
    #     "total": "",
    #     "number": "",
    #     "emp_id": "",
    #     "ticket_id": ""
    # }
    params = {}
    param = Entity.objects.filter(bot_id=bot_id)
    
    for para in param:
        params[para.entity_key] = ""
    print('inside reset',params)    
    return params


def check_parameters(conversation_id, parameters, bot_id):
    print('parameters-check', parameters)
    parameters = {k: str(v[0]) for k, v in parameters.items()}

    if ConversationParameters.objects.filter(conversation_id=conversation_id).first() is  None:
        conv_obj = ConversationParameters(conversation_id=conversation_id,
                                          parameters=reset_parameters_list(bot_id), time=datetime.datetime.now())
        conv_obj.save()

    # elif ConversationParameters.objects.filter(conversation_id=conversation_id).first() is not None:
    #     obj = ConversationParameters.objects.get(conversation_id=conversation_id)
    #     print('ConversationParameters',obj)
    #     obj.parameters=reset_parameters_list(bot_id)
    #     obj.save()


    conv_obj = ConversationParameters.objects.filter(conversation_id=conversation_id).first()
    conv_param = conv_obj.parameters
    print('inside-check',conv_param)
    for k, v in parameters.items():
        if k != "any" and k != "email" and k != "number" and k != 'emp_id':
            print("entity other than any email ", k, v)
            entity_list = Entity.objects.filter(entity_key=k, bot_id=bot_id)
            print("-------------------->---------------------------->",entity_list)

            entity_values = entity_list.filter(entity_synonyms__contains=v).first()
            if entity_values:
                print("-------------------->---------------------------->",entity_values)
                entity_val = entity_values.entity_value
                print('entity_val', entity_val)
                conv_param[k] = str(entity_val).upper()
            else:
                conv_param[k] = v
        else:
            print('entity_val-else-outside',v)
            conv_param[k] = v
    conv_obj.parameters = conv_param
    conv_obj.time = datetime.datetime.now()
    conv_obj.save()
    parameters = conv_param
    print(parameters)
    # parameters = {k: str(v[0]).upper() for k, v in parameters.items()}
    return parameters
