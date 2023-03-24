import json
import dialogflow_v2
from google.oauth2 import service_account
from google.api_core.exceptions import InvalidArgument
from google.protobuf.json_format import MessageToJson
from nlp_lib.dialogflow_client_manager import dialogflow_client_manager


def detect_intent(service_account_info, input_message, session_id):
    # credentials = service_account.Credentials.from_service_account_info(service_account_info)
    # session_client = dialogflow_v2.SessionsClient(credentials=credentials)\
    print('sent request to dialogflow')
    # try:
    # 0x05FE0BE0
    session_client = dialogflow_client_manager.get_client(service_account_info)
    dialogflow_language_code = 'en-US'
    session_id = session_id
    text_to_be_analyzed = input_message

    session = session_client.session_path(service_account_info['project_id'], session_id)
    text_input = dialogflow_v2.types.TextInput(text=text_to_be_analyzed, language_code=dialogflow_language_code)
    query_input = dialogflow_v2.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except Exception as e:
        response = session_client.detect_intent(session=session, query_input=query_input)
        print("dialogflow exception", e)
    return response
