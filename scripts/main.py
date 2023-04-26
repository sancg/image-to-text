import json
import os

from utils.capture import Capture
from utils.client_helper import ClientHandler

working_directory = os.getcwd()
file_path = f'{working_directory}/scripts/data/img/test4.jpg'
save_path = f'{working_directory}/scripts/data/response.json'

cl = ClientHandler(file_path, save_path).save_json_file()
raw_text = cl['ocr_text']
# print(raw_text)


capture = Capture('The american tobacco company', raw_text)

total_bills = capture.get_total_docs_process()
result = capture.extract_data()

file_path_results = f'{working_directory}/scripts/data/result_test.json'
with open(file_path_results, 'w') as _f:
    json.dump(result, _f, indent=4)
print(json.dumps(result, indent=4))
