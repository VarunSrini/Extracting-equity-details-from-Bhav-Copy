import redis
from io import BytesIO
from zipfile import ZipFile
import urllib.request
import re
import json
from datetime import date
from datetime import datetime, timedelta

redis_host = "localhost"
redis_port = 6379
redis_password = ""

r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

def isValidUrl(url):
    flag = 0

    try:
        urllib.request.urlopen(url).getcode()
        flag = 1
        #print("It works")
    
    finally:
        return(flag)
    
def getDate(date):
    finalDate = ''
    for i in date:
        if i == '/':
            continue
        finalDate = finalDate + i
    return finalDate[0:4] + finalDate[6:]
    


date = getDate(datetime.strftime(datetime.now() , "%d/%m/%Y"))

# The below loop checks if the url exists or not
count = 0
while(isValidUrl("https://www.bseindia.com/download/BhavCopy/Equity/EQ{}_CSV.ZIP".format(date)) != 1):
    #print("Not working")
    count = count + 1
    date = getDate(datetime.strftime(datetime.now() - timedelta(count), "%d/%m/%Y"))

#url = urllib.request.urlopen("https://www.bseindia.com/download/BhavCopy/Equity/EQ171019_CSV.ZIP")
url = urllib.request.urlopen("https://www.bseindia.com/download/BhavCopy/Equity/EQ{}_CSV.ZIP".format(date))


with ZipFile(BytesIO(url.read())) as my_zip_file:
    dataFromCsv = []
    for contained_file in my_zip_file.namelist():

        for line in my_zip_file.open(contained_file).readlines():
            dataFromCsv.append(str(line))

        extractedData = []
        flag = True
        
        for i in dataFromCsv:
            if(flag):
                flag = False
                continue
            
            li  = i.split(",")
            d = {} 
            
            code = li[0][2:]
            
            d["code"] = code    # code
            d["name"] = li[1].strip()   # name
            d["open"] = li[4]   # open
            d["high"] = li[5]   # high
            d["low"] = li[6]    # low
            d["close"] = li[7]  # close

            json_data = json.dumps(d)

            # Below  3 lines adds into redis
            r.set(d["name"],json_data)
            
            # This is a string data structure
            r.set(d["code"], d["name"])
            
            # This is a sorted set data structure
            r.zadd("equity", {d["code"]: float(d["close"])})
'''
# Below should be able to read from redis
print("****************************************")
code = r.zrevrange("equity", 0, 9)


for i in code:
    print(r.get(r.get(i)))
'''

        
















