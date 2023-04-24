import os
import json
from veryfi import Client

from dotenv import load_dotenv
# Setting up the working environment
# load the environment variable from the .env file
load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
username = os.getenv('USERNAME')
api_key = os.getenv('API_KEY')


class ClientHandler(Client):
    def __init__(self, docs_to_process: str, save_path: str):
        # super().__init__()
        self.client = Client(client_id, client_secret, username, api_key)
        self.save_path = save_path
        self.docs_to_process = docs_to_process
        self.save_json_file()

    def save_json_file(self) -> dict:
        """Make a request to process_document if save_path doesn't exist.
        And it saves a dictionary into the data folder as a json format.

        Args:
            store_json (dict): JSON dictionary generated from the Veryfi Client response.
            json_file_path (str, optional): Path directory including the name file. Defaults to './data/tmp/response.json'.
        """
        if not (os.path.exists(self.save_path)):
            response = self.client.process_document(self.docs_to_process)
            print('\033[95mprocessing Documents\033[0m\n')
            with open(self.save_path, 'w') as _f:
                json.dump(response, _f, indent=4)
            return response
        else:
            print('\033[93mJSON file already exists\033[0m\n')
            return self.read_json_file()

    def read_json_file(self) -> dict:
        with open(self.save_path, 'r') as _f:
            response = json.load(_f)
        return response
