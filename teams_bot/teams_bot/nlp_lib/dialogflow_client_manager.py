import json

import dialogflow_v2
from google.oauth2 import service_account


class DialogFlowClientManager:
    clients = {}

    def __init__(self):
        pass

    def get_client(self, service_account_info):
        client = self.clients.get(self.get_key(service_account_info))
        if not client:
            print("DIALOGFLOW CLIENT NOT FOUND: ADDING")
            self.add_client(service_account_info)
        client = self.clients.get(self.get_key(service_account_info))
        return client

    def add_client(self, service_account_info):
        if service_account_info:
            credentials = service_account.Credentials.from_service_account_info(service_account_info)
            client = dialogflow_v2.SessionsClient(credentials=credentials)
            self.clients[self.get_key(service_account_info)] = client

    @staticmethod
    def get_key(service_account_info):
        return service_account_info['project_id'] + '-' + service_account_info['private_key_id']


dialogflow_client_manager = DialogFlowClientManager()
print(json.dumps(list(dialogflow_client_manager.clients.keys())))
