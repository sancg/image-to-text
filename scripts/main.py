import json
import os
import re

from utils.capture import Capture 
from utils.client_helper import ClientHandler

working_directory = os.getcwd() 
file_path = f'{working_directory}/scripts/data/img/test4.jpg'
save_path = f'{working_directory}/scripts/data/response.json'

cl = ClientHandler(file_path, save_path).save_json_file();
raw_text = cl['ocr_text']
# print(raw_text)

# pattern_vendor_name = re.compile(r'^THE.*?\bCOMPANY\b', flags=re.M|re.S); 
pattern_vendor_name = re.compile(r".*\b(SPECIAL NOTICE)\b|^\b.*FORUM\b", flags=re.M);
# Use of re.DOTALL to match across multiple lines and treat the lines as single.
vendor_raw_name = pattern_vendor_name.split(raw_text)
# print(vendor_raw_name)


# result = list(vendor_raw_name)
# print((vendor_raw_name))
# for name in vendor_raw_name:
#     print(name)
#     print('\n')

total_bills = Capture(raw_text).get_total_docs_process()
print(total_bills)