import os

files = os.listdir('./result')
res = []
for file in files:
    if file != '.DS_Store':
        f = open('./result/'+file,'r').read()
        res.append(f)
output = open('result.json','a')
for i in res:
    print(i[:-1],file = output)