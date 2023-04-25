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


class ClientHandler():
    """Class Helper to store and retrieve Dictionaries as JSON format after been processed by the veryfi API

    Args:
        docs_to_process (str): path were the required documents are located.
        save_path (str): path to store the process_documents
    """
    def __init__(self, docs_to_process: str, save_path: str):
        self.client = Client(client_id, client_secret, username, api_key)
        self.save_path = save_path
        self.docs_to_process = docs_to_process
        

    def save_json_file(self) -> dict:
        """Make a request to process_documents if save_path doesn't exist, and it saves a dictionary into the data folder as a json format.
        If the save_path provided exists, then it will read the JSON file.
        """
        if not (os.path.exists(self.save_path)):
            response = self.client.process_document(self.docs_to_process)
            print('\033[95mprocessing Documents\033[0m\n')
            with open(self.save_path, 'w') as _f:
                json.dump(response, _f, indent=4)
            return response
        else:
            print('\033[93mJSON file already exists\033[0m\n')
            try:
                return self.read_json_file()
            except FileNotFoundError:
                print(f'The file {self.save_path} couldn\'t be read')

    def read_json_file(self) -> dict:
        with open(self.save_path, 'r') as _f:
            response = json.load(_f)
        return response
