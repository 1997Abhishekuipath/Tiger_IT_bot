# Create your views here.
import json

import requests
import urllib3
from google.protobuf.json_format import MessageToDict
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from bot.models.model_intents import Intent
from botData.models.model_bot_ratings import BotRating
from botData.models.model_fallbacks import FallbackMessage
from botData.models.model_feedback_form import Message, FeedbackForm
from botPlatform.models.model_botuser import BotUserInfo
from botPlatform.models.model_platform import Platform
from nlp_lib.dialogflow_apis import detect_intent
from nlp_lib.rasa_detect_intent import rasa_detect_intent
from teams.teams_template import teams_response


# urllib3.disable_warnings()
class TeamsWebhook(generics.GenericAPIView):
    permission_classes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request_data = None
        self.received_msg = None
        self.conversation_id = None
        self.user_aadID = None
        self.user_teams_id = None
        self.service_url = None
        self.platform = Platform.objects.filter(name='teams')

    def post(self, request):
        self.request_data = request.data
        # print(self.request_data)
        if self.request_data['type'] == 'messageReaction':
            return Response(status=status.HTTP_200_OK)
        elif self.request_data.get('text'):
            self.received_msg = self.request_data['text']
            # To remove mentioned bot name ('<at>ticketer</at>', '') from text
            if self.request_data['entities'][0].get('mentioned'):
                self.received_msg = self.received_msg.replace(
                    '<at>{}</at>'.format(self.request_data['entities'][0]['mentioned']['name']), '')
            print(self.received_msg)
            self.teams_data = self.process_teams_data()
            self.save_message(msg_type='user', is_feedback=False, msg=self.received_msg)
            self.nlp_agent = self.bot_id.nlp_agent
            if self.nlp_agent.type == 'rasa':
                response_msg = self.rasa_api()
            elif self.nlp_agent.type == 'dialogflow':
                response_msg = self.dialogflow_api()
            self.save_message(msg_type='bot', is_feedback=False, msg=response_msg)
            # print(url)
            # res = self.send_message(message, url)

        else:
            self.teams_data = self.process_teams_data()
            url = '{}v3/conversations/{}/activities'.format(self.service_url, self.conversation_id)
            response_msg = teams_response(msg={"text": "Thanks for your time. Have a nice day."}, params={})
            print(request.data)
            if request.data.get('value').get('feedback'):
                feedback = request.data['value']['feedback']
                self.save_message(msg_type='user', is_feedback=True, msg=feedback)
                # userfeedback = UserFeedback(username=user_data.name, useremail=user_data.email_address,
                #                             feedback=feedback)
                # userfeedback.save()
            elif request.data.get('value').get('selected_date'):
                pass
            elif request.data.get('value').get('bot_rating'):
                rating = request.data.get('value').get('bot_rating')
                rate_obj = BotRating(bot_id=self.bot_id, user_id=self.teams_user, rating=rating)
                rate_obj.save()
                msg = Intent.objects.filter(name="feedback").first().response
                response_msg = teams_response(msg, params={})
            elif request.data.get('value').get('ticketDescription'):
                print(request.data)
                params = {
                    'ticket_id': request.data.get('value').get('incident_no'),
                    'description': request.data.get('value').get('ticketDescription'),
                    'summary': request.data.get('value').get('summary')
                }
                response_msg = self.webhook_call(intent_name='update_ticket', parameters=params)

        if not response_msg:
            response_msg = teams_response(msg={"text": "Hi, an error occurred please try again."}, params={})

        self.send_message(message=response_msg)
        return Response(status=status.HTTP_200_OK)

    def process_teams_data(self):
        print(self.request_data)
        self.conversation_id = self.request_data['conversation']['id']
        self.user_aadID = self.request_data['from']['aadObjectId']
        self.user_teams_id = self.request_data['from']['id']
        self.service_url = self.request_data['serviceUrl']
        self.bot_name = self.request_data['recipient']['name']
        teams_bot_id = self.request_data['recipient']['id']
        teams_bot_id = teams_bot_id[3:]
        self.platform_info = Platform.objects.filter(config__contains={"app_id": teams_bot_id}).first()
        self.bot_id = self.platform_info.bot_id
        if BotUserInfo.objects.filter(info__contains={'user_teams_id': self.user_teams_id}).first():
            self.teams_user = BotUserInfo.objects.filter(info__contains={'user_teams_id': self.user_teams_id}).first()
            # = BotUserInfo.objects.filter(info__contains={'user_teams_id': self.user_teams_id}).first()
        else:
            self.teams_user = self.user_details()
        self.user_email = self.teams_user.email
        return self.teams_user

    def save_message(self, msg, msg_type, is_feedback=False, ):
        if is_feedback:
            msg_id = Message.objects.filter(user_id=self.teams_user, type='user').order_by('-updated_at')[1]
            user_msg = FeedbackForm(user_message=msg, bot_id=self.bot_id, user_id=self.teams_user, message_id=msg_id)
        else:
            user_msg = Message(type=msg_type, message=msg, bot_id=self.bot_id, user_id=self.teams_user)
        user_msg.save()
        return user_msg

    def send_message(self, message):
        url = '{}v3/conversations/{}/activities'.format(self.service_url, self.conversation_id)
        try:
            token = self.platform_info.config.get('access_token')
            if not token:
                token = self.get_token()
            msgs = message
            for msg in msgs:
                payload = json.dumps(msg)
                headers = {
                    'Authorization': 'Bearer {}'.format(token),
                    'Content-Type': 'application/json'
                }
                response = requests.post(url=url, headers=headers, data=payload, verify=False)
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                print(response.text.encode('utf8'))
            if response.status_code == 401:
                token = self.get_token()
                msgs = message
                for msg in msgs:
                    payload = json.dumps(msg)
                    headers = {
                        'Authorization': 'Bearer {}'.format(token),
                        'Content-Type': 'application/json'
                    }
                    response = requests.post(url=url, headers=headers, data=payload, verify=False)
                    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                    print(response.text.encode('utf8'))
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            print('sent message response', response.text.encode('utf8'))
        except Exception as e:
            print('exception', e)
        return response

    def get_token(self):
        try:
            url = "https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token"

            payload = 'grant_type=client_credentials&client_id={}&client_secret={}&scope=https%3A//api.botframework.com/.default'.format(
                self.platform_info.config['app_id'], self.platform_info.config['app_secret'])
            headers = {
                'Host': 'login.microsoftonline.com',
                'Content-Type': 'application/x-www-form-urlencoded',
            }

            response = requests.post(url=url, headers=headers, data=payload, verify=False)
            print(response.text)
            print("response is ", response)
            res = json.loads(response.text)
            token = res['access_token']
            teams_obj = self.platform_info
            teams_obj.config['access_token'] = token
            teams_obj.save()
            return token

        except:
            print(Exception)

    def user_details(self):
        # print(self.service_url, self.conversation_id, self.user_teams_id)
        url = '{}v3/conversations/{}/members/{}'.format(self.service_url, self.conversation_id, self.user_teams_id)
        try:
            token = self.platform_info.config.get('access_token')
            if not token:
                token = self.get_token()
            headers = {
                'Authorization': 'Bearer {}'.format(token),
                'Content-Type': 'application/json'
            }
            response = requests.get(url=url, headers=headers, verify=False)
            if response.status_code == 401:
                token = self.get_token()
                headers = {
                    'Authorization': 'Bearer {}'.format(token),
                    'Content-Type': 'application/json'
                }
                response = requests.get(url=url, headers=headers, verify=False)
                print(response.text)
            print('user info', response.text)
            user_data = json.loads(response.text)
            user_email = user_data['email']
            user_name = user_data['name']
            user_aad_id = user_data['aadObjectId']
            user = BotUserInfo(name=user_name, email=user_email,
                               info={"user_aad_id": user_aad_id, "user_teams_id": self.user_teams_id},
                               platform_id=self.platform_info)
            user.save()
            print(user)
            return user

        except Exception as e:
            print('exception', e)

    # / v3 / conversations / {conversationId} / members / {userId}

    # requests.get('https://kennethreitz.com', verify=True)

    def webhook_call(self, intent_name, parameters):
        intent_url = Intent.objects.filter(name=intent_name, bot_id=self.bot_id).first().webhook
        webhook_url = intent_url['webhook_url']
        # webhook_url = 'http://10.83.145.69:8020/webhook/service'
        body = {
            "intent_name": intent_name,
            # "teams_email": self.user_email,
            "teams_email": "mansi.gupta.ff@hitachi-systems.com",
            # "teams_email": "neha.turan.ec@hitachi-systems.com",
            # "teams_email": "Jay.khanna.ep@hitachi-systems.com",
            "parameters": parameters,
            "user_query": self.received_msg,
            "flow_name": intent_name
        }

        payload = json.dumps(body)
        print(payload)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url=webhook_url, headers=headers, data=payload, verify=False)
        print('webhook response', response.text.encode('utf8'))
        out_response = json.loads(response.text)['response'] if response != "{}" else "{'text':'hi'}"
        out_message = teams_response(msg=out_response, params=parameters)
        return out_message

    def dialogflow_api(self):
        print('dialogflow hit')
        service_account_info = self.nlp_agent.config
        try:
            intent_res = detect_intent(service_account_info=service_account_info, input_message=self.received_msg,
                                       session_id=self.conversation_id)
            df_intent = intent_res.query_result.intent.display_name
            df_parameters = intent_res.query_result.parameters
            context = None
            if intent_res.query_result.output_contexts:
                output_context = intent_res.query_result.output_contexts
                list_key = []
                for i in output_context:
                    key_len = len(i.parameters.keys())
                    list_key.append(key_len)
                max_key = list_key.index(max(list_key))
                context = output_context[max_key].parameters
                # context = intent_res.query_result.output_contexts[len(intent_res.query_result.output_contexts)-1].parameters
            parameters = context if context is not None else df_parameters
            print(df_intent)

            # db_intent = Intent.objects.get(name=df_intent)
            db_intent = Intent.objects.get(name=df_intent, bot_id=self.bot_id)
            if intent_res.query_result.all_required_params_present:
                if db_intent.name == 'nlu_fallback' or db_intent.name == 'Default Fallback Intent' or db_intent.name == 'Default FallbackIntent' and not self.user_verified == 'false':
                    msg_id = Message.objects.filter(user_id=self.teams_user, type='user').last()
                    store_fallback_msg = FallbackMessage(bot_id=self.bot_id, user_id=self.teams_user, message_id=msg_id)
                    store_fallback_msg.save()
                # if db_intent.name == 'thanks':
                #     response_msg = adaptive_card
                #     # response_msg = calender_card_template
                if db_intent.response:
                    print('database call')
                    response_msg = teams_response(msg=db_intent.response, params=parameters)
                elif db_intent.webhook:
                    print('webhook call')
                    parameters = MessageToDict(parameters)
                    response_msg = self.webhook_call(intent_name=df_intent, parameters=parameters)
            elif not intent_res.query_result.all_required_params_present:
                fulfillment_msg = {"text": intent_res.query_result.fulfillment_text}
                response_msg = teams_response(msg=fulfillment_msg, params={})
        except Exception as e:
            print(e)
            response_msg = teams_response(msg={"text": "Hi, an error occured please try again."}, params={})
        # response_msg = temp
        return response_msg

    def rasa_api(self):
        try:
            res = rasa_detect_intent(self.received_msg, self.conversation_id, self.bot_id)
            intent_res = res['intent_res']
            df_intent = intent_res['queryResult']['intent']['displayName']
            parameters = res['parameters']
            db_intent = Intent.objects.get(name=df_intent, bot_id=self.bot_id)
            if db_intent.name == 'nlu_fallback' or db_intent.name == 'Default Fallback Intent' or db_intent.name == 'Default FallbackIntent' and not self.user_verified == 'false':
                msg_id = Message.objects.filter(user_id=self.teams_user, type='user').last()
                store_fallback_msg = FallbackMessage(bot_id=self.bot_id, user_id=self.teams_user, message_id=msg_id)
                store_fallback_msg.save()

            # if db_intent.name == 'thanks':
            #     response_msg = adaptive_card
            #     # response_msg = calender_card_template
            if db_intent.response:
                print('database call')
                response_msg = teams_response(msg=db_intent.response, params=parameters)
            elif db_intent.webhook:
                print('webhook call')
                response_msg = self.webhook_call(intent_name=df_intent, parameters=parameters)
        except Exception as e:
            print(e)
            response_msg = teams_response(msg={"text": "Hi, an error occured please try again."}, params={})

        return response_msg
