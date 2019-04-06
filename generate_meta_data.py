import os
import json

## Arguments
NOTEBOOK_DIR = ""
DIR_STATIC = "files"
MODULE_ID = 63600
TAGS = "BC"
COMMON_CODE_URL = ""
AUTHOR = "Aravind Sankaran"

# setting this to false will over-write code_urls.txt and your changes will be lost
CODE_URLS_REUSE = False

MODULE_NAME =  os.getcwd().split('/')[-1]
# Relative path. leave it blank if notebook files are in current dir
NOTEBOOK_DIR = os.path.join(os.getcwd(),NOTEBOOK_DIR)

configs = {}

configs["dir_path"] = NOTEBOOK_DIR
configs["dir_static"] = DIR_STATIC
configs["module_name"] = MODULE_NAME
configs["module_id"] = MODULE_ID
configs["author"] = AUTHOR
configs["tags"] = TAGS

def get_list_all_files_name(dir_path):
    all_files_path = []
    dnt = []
    if os.path.exists(os.path.join(dir_path, "DoNotTrack")):
        dnt = open(os.path.join(dir_path, "DoNotTrack"), 'r').read().split()
        # print(dnt)
    for f in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, f)):
            if f.endswith('.ipynb') or f.endswith('.pdf'):
                if f not in dnt:
                    all_files_path.append(os.path.join(f))

    return all_files_path


def parse_code_urls():
   with open('code_urls.txt', 'r') as f:
      while(True):
         x = f.readline().strip()
         if x is "":
            return
         y = f.readline().strip()
         configs[x]['code_url'] = y
         f.readline()

file_list = get_list_all_files_name(NOTEBOOK_DIR)
file_list.sort()


configs['file_list'] = file_list

for f in file_list:
    configs[f] = {}


page_id = 1
code_urls_txt = ""
for f in file_list:
    page_name = f.split('.ipynb')[0]
    pdf = False
    if ".pdf" in page_name:
       pdf = True
       page_name = page_name.split(".pdf")[0]
    code_url = ""
    if os.path.exists(os.path.join(os.getcwd(),page_name)):
        code_url = "https://github.com/as641651/" + MODULE_NAME + "/tree/master/" + page_name

    if COMMON_CODE_URL != "":
        code_url = COMMON_CODE_URL

    configs[f]["code_url"] = code_url
    configs[f]["page_name"] = page_name
    configs[f]["pdf"] = pdf
    configs[f]["page_id"] = MODULE_ID + page_id
    
    page_id = page_id+1
    code_urls_txt += f + "\n" + code_url + "\n\n"

# overwrite code urls from cache
if CODE_URLS_REUSE:
    parse_code_urls()
else:
    with open('code_urls.txt', 'w') as f:
        f.write(code_urls_txt)
    
with open('configs.json', 'w') as outfile:
    json.dump(configs, outfile, indent=4, sort_keys=True)

print(configs)
