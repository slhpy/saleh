import random
import re
from time import sleep
import json
import requests
from bs4 import BeautifulSoup

def get_numbers():
        global cz ,random_line
    
        with open('france.txt', 'r') as f:
            lines = f.readlines()

        # انتخاب رندوم یک خط
        random_line = random.choice(lines)
        cz = int(random_line)
        print(cz)
        # چاپ خط انتخاب شده

        return int(random_line)
    

    





def get_code():
    





    
    for i in range(2):
        try:
            
            
            url=f'https://otp-api.shelex.dev/api/France/{cz}?source=receive-sms-free.cc'
            print(url)
            respons = requests.get(url=url , timeout=30)

            s = respons.text
            w = json.loads(s)

# استخراج مقدار 'otp'
            result = w["result"]["otp"]

            if result != None :

                return result



            

        except:
            pass

           
