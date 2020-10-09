import sys
import os
import json
import requests
import ipdb
import re
import tqdm

#res = [{'title':,'pubilsher':,'pDate':,'source':,'oss_url':,'text':,'commit':}]
res = []
source = 'yanbao'
commit = 'Zhiwei Hu' + '2020-10-09'
url = 'http://broker.aigauss.com:8007/management/file/tables'
file_path = './半导体/'

def process_file(file_path):
    file_list = []
    files = os.listdir(file_path)
    for file in files:
        file_list.append(file)
    return file_list

def main(res,file_list):
    temp = {}
    headers = {}
    payload = {}
    for file in file_list:
        temp['title'] = file.split('：')[0]
        files = [
            ('file', open(file_path+file,'rb'))
        ]
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        temp['text'] = json.loads(response.text)
        temp['publisher'] = ''.join(re.findall('[^0-9.]',(file.split('-')[-2])))
        date = re.findall('[0-9.]+',file)[-3]
        temp['pDate'] = date if date != '9014' else '2019.12.3'
        temp['source'] = source
        temp['oss_url'] = url
        temp['commit'] = commit
        result = json.dumps(temp, ensure_ascii=False)
    res.append(result)
    output = open('semiconductor.json', 'w')
    for i in res:
        print(i,file = output)


if __name__ == '__main__':
    file_list = process_file(file_path)
    main(res,file_list)