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
commit = 'Zhiwei Hu ' + '2020-10-09'
url = 'http://broker.aigauss.com:8007/management/file/tables'
file_path = './半导体/'

def process_file(file_path):
    file_list = []
    files = os.listdir(file_path)
    for file in files:
        if file != '.DS_Store' :
            file_list.append(file)
    return file_list

def main(res,file_list,output_file):
    cnt = 0
    for file in file_list:
        temp = {}
        title = file.split('：')[0]
        temp['title'] = title
        files = [
            ('file', open(file_path+file,'rb').read())
        ]
        response = requests.request("POST", url,files=files)
        text = json.loads(response.text)
        temp['text'] = text
        print(cnt)
        publisher = file.split('-')[-2]
        #temp['publisher'] = ''.join(re.findall('[^0-9.]',(file.split('-'))[-2]))
        temp['publisher'] = publisher if len(publisher) < 6 else ''
        date_temp = re.findall('[0-9.]+',file)
        for date in date_temp:
            real_date = date_temp[0]
            if len(date) > len(real_date):
                real_date = date
        temp['pDate'] = real_date
        #temp['pDate'] = date if date != '9014' else '2019.12.3'
        temp['source'] = source
        temp['oss_url'] = url
        temp['commit'] = commit
        cnt += 1
        result = json.dumps(temp, ensure_ascii=False)
        res.append(result)
    output = open(output_file,'w')
    for i in res:
        print(i,file = output)


"""def test(file_list):
    temp = {}
    for file in file_list:
        publisher = file.split('-')[-2]
        #temp['publisher'] = ''.join(re.findall('[^0-9.]',(file.split('-'))[-2]))
        temp['publisher'] = publisher if len(publisher) < 6 else ''
        print(temp)"""


if __name__ == '__main__':
    # file_path = './pdf/'
    # output = 'new.json'
    file_path = sys.argv[1]
    output = sys.argv[2]
    res = []
    file_list = process_file(file_path)
    main(res,file_list,output)
    #test(file_list)