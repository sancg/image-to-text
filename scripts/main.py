import json

from utils.helper import ClientHandler

file_path = './scripts/data/documents_to_process.zip'
save_path = './scripts/data/response.json'
cl = ClientHandler(file_path, save_path)
json_response = cl.read_json_file()

print(json_response['ocr_text'])
