from email import message
import json
import time
from os.path import exists
from balecode import *
import re 
from bs4 import BeautifulSoup
from protobuf import decode_proto, encode_proto
import random
from fake_useragent import UserAgent
from fake_useragent import UserAgent
ua = UserAgent()
import cloudscraper
requests = cloudscraper.create_scraper(disableCloudflareV1=True)  # returns a CloudScraper instance

class Bot:
    
    def __init__(self, botname, auto_login=False) -> None:
        if exists(f"./token/{botname}.json") == True:
            with open(f"./token/{botname}.json", 'r') as f:
                self.token = (json.load(f)).get('token')
        else:
            if auto_login == True:
                Bot.__auto_login(self, botname)
            else:
                Bot.__login(self, botname=botname,
                          number=input('What is your number?'))

    def __login(self, botname, number):
        code_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.auth.v1.Auth/StartPhoneAuth",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-length": "148",
            "content-type": "application/grpc-web-text",
            "cookie": "_ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1",
        }

        code_token = (dict(decode_proto(requests.post(url='https://next-api.bale.ai/bale.auth.v1.Auth/StartPhoneAuth', data=encode_proto({'1:0': int(
            number), '2:0': 4, '3:2': 'C28D46DC4C3A7A26564BFCC48B929086A95C93C98E789A19847BEE8627DE4E7D', '4:2': 'Chrome, Linux', '5:2': 'Chrome, windows', '9:0': 0}), headers=code_headers).text))).get('1:2')
        print(code_token)

        login_code = input('login code?')
        token = requests.post(url='https://next-api.bale.ai/bale.auth.v1.Auth/ValidateCode', data=encode_proto(
            {'1:2': code_token, '2:2': login_code, '3:2': {'1:0': 1}}), headers=code_headers).text

        if bool(token) == False:
            token = ((dict(decode_proto(requests.post(url='https://next-api.bale.ai/bale.auth.v1.Auth/SignUp',
                     data=encode_proto({'1:2': code_token, '2:2': botname}), headers=code_headers).text))).get('4:2')).get('1:2')
                     
        else:
            token = ((dict(decode_proto(token))).get('4:2')).get('1:2')

        self.token = token
        print(self.token)

        with open(f"./token/{botname}.json", 'w') as f:
            json.dump({"token": number, "token": token}, f)

        return self.token

    def import_contacts(self, number, contact_name):
        contacts = encode_proto(
            {'1:2': {'1:0': int(number), '2:2': {'1:2': str(contact_name)}}})
        import_contacts_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.users.v1.Users/ImportContacts",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-length": f"{len(contacts)}",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "session_id": "8604562129028668",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        self.contacts_id = ((dict(decode_proto(requests.post(url='https://next-api.bale.ai/bale.users.v1.Users/ImportContacts',
                            data=contacts, headers=import_contacts_headers).text))).get('4:2')).get('1:0')

        return self.contacts_id
    def invite_user(self, contacts_id, channel_id):


        user_invite = encode_proto({'1:2': {'1:0': channel_id, "2:0":1000} ,'3:2': {'1:0': int(contacts_id)} , "9:0":10})
        invite_user_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.users.v1.Users/ImportContacts",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-length": f"{len(user_invite)}",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "session_id": "8604562129028668",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-api.bale.ai/bale.groups.v1.Groups/InviteUser',
                      data=user_invite, headers=invite_user_headers).text

    def __auto_login(self, botname):
        code_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.auth.v1.Auth/StartPhoneAuth",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "origin": "https://web.bale.ai",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "x-grpc-web": "1",
            "x-user-agent": ua.random
        }
 

        numbera = get_numbers()
        number = f"{numbera}"
        a = ["samsung" , "lenovo" , "windows" , "linu" , "ubuntu",'chorme','xfde','sony' ]
        b = ['sergf'  , 'ftasdfu' ,    'ftqeu','awdadwaw','awdawdaw','awdawdsddad']
        a1  = random.choice(a)
        b1 = random.choice(b)
        from x import qq
        print(qq)
        code_token =(dict(decode_proto(requests.post(url='https://next-api.bale.ai/bale.auth.v1.Auth/StartPhoneAuth', data=encode_proto({'1:0': int(
        number), '2:0': 3, '3:2': 'C28D46DC4C3A7A26564BFCC48B929086A95C93C98E789A19847BEE8627DE4E7D', '4:2': f'5c6c9053e50e1efe3268a6a6cf56a46e',  '9:0': 0}), headers=code_headers).text))).get('1:2')
        print(code_token)
        login_code = str(get_code())

        token = requests.post(url='https://next-api.bale.ai/bale.auth.v1.Auth/ValidateCode', data=encode_proto(
            {'1:2': code_token, '2:2': login_code, '3:2': {'1:0': 1}}), headers=code_headers).text

        if bool(token) == False:
            token = ((dict(decode_proto(requests.post(url='https://next-api.bale.ai/bale.auth.v1.Auth/SignUp',
                     data=encode_proto({'1:2': code_token, '2:2': botname}), headers=code_headers).text))).get('4:2')).get('1:2')
                     
        else:
            token = ((dict(decode_proto(token))).get('4:2')).get('1:2')

        self.token = token
        print(self.token)

        with open(f"./token/{botname}.json", 'w') as f:
            json.dump({"number": number, "token": token}, f)

        return self.token


    def send_message(self, text, user_id):                
                message = encode_proto(
        {
            '1:2': {'1:0': 1, '2:0': user_id}, 
            '2:0': int(str(
            time.time()).replace(".", "")[:13]),  
            '3:2': {"15:2":{"1:2":text}}})
                print(message)
                send_message_headers={

                "authority": "next-api.bale.ai",
                "method": "POST",
                "path": "/bale.users.v1.Users/ImportContacts",
                "scheme": "https",
                "accept": "application/grpc-web-text",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
                "content-type": "application/grpc-web-text",
                "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
                "origin": "https://web.bale.ai",
                "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "Linux",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "session_id": "8604562129028668",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "x-grpc-web": "1",
                "x-user-agent": "grpc-web-javascript/0.1"
            }

                return requests.post(url='https://next-api.bale.ai/bale.messaging.v2.Messaging/SendMessage',
                        data=message, headers=send_message_headers).text
    
    def get_login_code(self):
        getcode = encode_proto({'1:2': {'1:0': 1, '2:0': 10}, '2:0': int(str(
            time.time()).replace(".", "")[:13]), '4:0': 2, '5:0': 20})

        get_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.users.v1.Users/ImportContacts",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-length": f"{len(getcode)}",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "session_id": "8604562129028668",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        messages = (dict(decode_proto(requests.post(url='https://next-api.bale.ai/bale.messaging.v2.Messaging/LoadHistory',
                                                    data=getcode, headers=get_message_headers).text))).get('1:2')
        for i in messages:
            return i.get('4:2').get('15:2').get('1:2')

    def get_messages(self, user_id):
        getmessage = encode_proto({'1:2': {'1:0': 1, '2:0': 10}, '2:0': int(str(
            time.time()).replace(".", "")[:13]), '4:0': 2})

        get_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.users.v1.Users/ImportContacts",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-length": f"{len(getmessage)}",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "session_id": "8604562129028668",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return  (requests.post(url='https://next-api.bale.ai/bale.messaging.v2.Messaging/LoadHistory',
                                                    data=getmessage, headers=get_message_headers).text)

    def get_sessions(self):

        get_sessions_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.users.v1.Users/ImportContacts",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-length": f"{len('AAAAAAA=')}",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "session_id": "8604562129028668",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        sessions = (dict(decode_proto(requests.post(url='https://next-api.bale.ai/bale.auth.v1.Auth/GetAuthSessions',
                                                    data='AAAAAAA=', headers=get_sessions_headers).text)))
        return sessions.get('1:2')

    def terminatet_sessions(self):
        get_sessions_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.users.v1.Users/ImportContacts",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-length": f"{len('AAAAAAA=')}",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "session_id": "8604562129028668",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        requests.post(url='https://next-api.bale.ai/bale.auth.v1.Auth/TerminateAllSessions',
                                                    data='AAAAAAA=', headers=get_sessions_headers)
        return True
    def joinChaneel(self, users_id):
        data = encode_proto(
            {'1:2': {'1:0': 1, '2:0': int(users_id)}})


        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-api.bale.ai/bale.groups.v1.Groups/JoinPublicGroup',
                      data=data, headers=send_message_headers).text

    def EditName(self, text):
        data = encode_proto({'1:2': str(text)})


        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.users.v1.Users/EditName",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }
        return requests.post(url='https://next-api.bale.ai/bale.users.v1.Users/EditName',
                      data=data, headers=send_message_headers).text

      
    

    def EditAbout(self, text):
        data = encode_proto({'1:2': {'1:2': text}})


        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.users.v1.Users/EditAbout",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-api.bale.ai/bale.users.v1.Users/EditAbout',
                      data=data, headers=send_message_headers).text



    def ReactToStory(self, storyId , text):
            data = encode_proto({'1:2':storyId, "2:2":text})

            send_message_headers = {
                "authority": "next-api.bale.ai",
                "method": "POST",
                "path": "/bale.story.v1.Story/reactToStory",
                "scheme": "https",
                "accept": "application/grpc-web-text",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
                "content-type": "application/grpc-web-text",
                "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
                "origin": "https://web.bale.ai",
                "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "Linux",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "x-grpc-web": "1",
                "x-user-agent": "grpc-web-javascript/0.1"
            }

            return requests.post(url='https://next-api.bale.ai/bale.story.v1.Story/ReactToStory',
                        data=data, headers=send_message_headers).text
            
    
 



    def LoadFullUser(self, user_id ):
        data = encode_proto(
            {'1:2': {"1:0":user_id , "2:0":1}})


        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054s.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return (requests.post(url='https://next-api.bale.ai/bale.users.v1.Users/LoadUsers',
                      data=data, headers=send_message_headers).text)




        
        

        



    def GetFullGroup(self, user_id ):
        data = encode_proto(
           {"1:2":{"1:0":int(user_id) , "2:0":1}})


        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return (requests.post(url='https://next-api.bale.ai/bale.groups.v1.Groups/GetFullGroup',
                      data=data, headers=send_message_headers).text)
        
        
        
        
    def LoadMember(self, user_id  , i):
        data = encode_proto(
           {"1:2":{ '1:0': int(user_id)} , "2:0":i})


        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return (requests.post(url='https://next-api.bale.ai/bale.groups.v1.Groups/LoadMembers',
                      data=data, headers=send_message_headers).text)
        
    def joinGroup(self, text):
        data = encode_proto(
            {'1:2':  text})


        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-api.bale.ai/bale.groups.v1.Groups/JoinGroup',
                      data=data, headers=send_message_headers).text
        
        
        
    def EditGroupTitle(self, text,user_id):
        data = encode_proto(
            {"1:2":{ '1:0': int(user_id) , "2:0":2} , "3:2":text})


        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-api.bale.ai/bale.groups.v1.Groups/EditGroupTitle',
                      data=data, headers=send_message_headers).text
        
        
        
        
        




    def GetUsersDefaultCardNumber(self,user_id):
        data = encode_proto(
            {"1:2":{ '2:0': int(user_id)}})


        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-api.bale.ai/bale.users.v1.Users/GetUsersDefaultCardNumber',
                      data=data, headers=send_message_headers).text
        




    def GetContacts(self,user_id):
        data = encode_proto(
            {"1:2":{ '2:0': int(user_id)}})


        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-api.bale.ai/bale.users.v1.Users/GetContacts',
                      data=data, headers=send_message_headers).text
        

    def SearchContacts(self,user_id):
        data = encode_proto(
            {'1:2': user_id})


        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-api.bale.ai/bale.users.v1.Users/SearchContacts',
                      data=data, headers=send_message_headers).text
        




    def GetMessagesReactions(self,user_id , msgid , time):
        data = encode_proto(
           {'1:2': {'1:0': 2, '2:0': int(user_id) } ,'2:2': {'1:0': int(time) , "2:0": int(msgid)}})

        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-api.bale.ai/bale.abacus.v1.Abacus/LoadReactions',
                      data=data, headers=send_message_headers).text
        

    def GetMessagesViews(self,user_id , msgid , time):
        data = encode_proto(
           {'1:2': {'1:0': 2, '2:0': int(user_id) } ,'2:2': {'1:0': int(time) , "2:0": int(msgid)}})


        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-api.bale.ai/bale.abacus.v1.Abacus/GetMessagesViews',
                      data=data, headers=send_message_headers).text






    def LeaveGroup(self, users_id):
        data = encode_proto(
            {'1:2': {'1:0': int(users_id)}})


        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-api.bale.ai/bale.groups.v1.Groups/LeaveGroup',
                      data=data, headers=send_message_headers).text


    def GetChannelStories(self, users_id ):
        data = encode_proto(
            {'1:2': {'2:0': int(users_id) , "1:0":3}})


        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return (requests.post(url='https://next-api.bale.ai/bale.story.v1.Story/GetStoriesByList',
                      data=data, headers=send_message_headers).text)





    def loadhistory(self , chat_id):
        getcode = encode_proto({'1:2': {'1:0': 2, '2:0': int(chat_id)}, '2:0': int(str(
            time.time()).replace(".", "")[:13]), '4:0': 2, '5:0': 1})


        

        get_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.users.v1.Users/ImportContacts",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "session_id": "8604562129028668",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return  (dict(decode_proto(requests.post(url='https://next-api.bale.ai/bale.messaging.v2.Messaging/LoadHistory',
                                                    data=getcode, headers=get_message_headers).text))).get("1:2")

        







    def ForwardMessages(self , user1 , user2 , msgid,t):
        getcode = encode_proto({'1:2': {"1:0":1 , '2:0': int(user1)} ,"2:0":int(str(time.time()).replace(".", "")[:13]), "3:2":{"1:2":{"1:0":2 , "2:0":int(user2)} , "2:0":int(msgid) , "3:2" :{"1:0":t}}})

        get_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.users.v1.Users/ImportContacts",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "session_id": "8604562129028668",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return (requests.post(url=' https://next-api.bale.ai/bale.messaging.v2.Messaging/ForwardMessages',
                                                    data=getcode, headers=get_message_headers).text)



    def CreateGroup(self , x):
        i=999999999999999999
        getcode = encode_proto({"1:0":999999999999999999 , "2:2":"i" , "3:2":{"1:0":1 , "2:0":i} , "6:0":i  , "8:2":{"1:2":"" , "5:0":i} , "9:0":i , "15:0":i , "22:0":i , "100:0":i})

        get_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.users.v1.Users/ImportContacts",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "session_id": "8604562129028668",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1",

        }

        return (requests.post(url='https://next-ws.bale.ai/bale.groups.v1.Groups/CreateGroup',
                                                    data=getcode, headers=get_message_headers).text)





    def SendInlineCallBackData(self):
        data = encode_proto(
            {"1:2":{"1:2":{"1:0":2,"2:0":1833181059} ,"2:0":9977836104796993001,"3:0":1712651232019}})
        get_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.users.v1.Users/ImportContacts",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "session_id": "8604562129028668",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1" , 

        }

        return (requests.post(url='https://next-ws.bale.ai/bale.magazine.v1.Magazine/UpvotePost',
                                                    data=data, headers=get_message_headers).text)




    def UpvotePost(self , id , msgid , t):
        data = encode_proto(
           {"1:2": {'1:2': {'1:0': 2, '2:0': id} ,'2:0': msgid, "3:0": t}})

        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-ws.bale.ai/bale.magazine.v1.Magazine/UpvotePost',
                      data=data, headers=send_message_headers).text
    def MessageSetReaction(self,user_id , msgid , time , emoji):
        data = encode_proto(
           {'1:2': {"1:0":2, '2:0': int(user_id) } ,'2:0': msgid ,"3:2":emoji ,  "4:0": int(time)})

        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-api.bale.ai/bale.abacus.v1.Abacus/MessageSetReaction',
                      data=data, headers=send_message_headers).text
        


    def lockGroup(self,user_id ,):
        data = encode_proto(
           {'1:2': {"1:0":user_id, '2:0': 1 } ,'2:2': {"1:0":1 , "5:0":1 , "9:0":1 , "11:2":{} , "12:2":{} , "13:2":{},"14:2":{"1:0":1} ,"15:2":{"1:0":1} ,"16:2":{"1:0":1},"17:2":{"1:0":1} , "18:2":{"1:0":1},"19:2":{}}})

        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-api.bale.ai/bale.groups.v1.Groups/SetGroupDefaultPermissions',
                      data=data, headers=send_message_headers).text
        

    def unlockGroup(self,user_id ,):
        data = encode_proto(
           {'1:2': {"1:0":user_id, '2:0': 1 } ,'2:2': {"1:0":1 , "5:0":1 ,"8:0":1, "9:0":1 , "11:2":{"1:0":1} , "12:2":{"1:0":1} , "13:2":{},"14:2":{"1:0":1} ,"15:2":{"1:0":1} ,"16:2":{"1:0":1},"17:2":{"1:0":1} , "18:2":{"1:0":1},"19:2":{}}})

        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-api.bale.ai/bale.groups.v1.Groups/SetGroupDefaultPermissions',
                      data=data, headers=send_message_headers).text


    def KickUser(self,user_group, user_kick):
        data = encode_proto(
           {'1:2': {"1:0":int(user_group), '2:0': 1},"4:0":int(str(
            time.time()).replace(".", "")[:13]) ,'3:2': {"1:0":int(user_kick) , "2:0":1 } , "5:2":""})

        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-api.bale.ai/bale.groups.v1.Groups/KickUser',
                      data=data, headers=send_message_headers).text
        
    def DeleteMessage(self,user_group, msgid , time):
        data = encode_proto(
           {'1:2': {"1:0":2, '2:0': user_group},"2:0":msgid,'3:2': {"1:0":time} , "4:2":""})
#{'1:0': 1852138519, '2:0': 2741825134347196488, '3:0': 1714158115584, '4:2': {'15:2': {'1:2': 'ی'}}, '10:2': {'1:0': 1714157856222, '2:0': 12792284568018499312}}
        send_message_headers = {
            "authority": "next-api.bale.ai",
            "method": "POST",
            "path": "/bale.messaging.v2.Messaging/MessageRead",
            "scheme": "https",
            "accept": "application/grpc-web-text",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7",
            "content-type": "application/grpc-web-text",
            "cookie": f"ga=GA1.1.1677184054.1678649765; _ga_M7ZV898665=GS1.1.1678691539.2.0.1678691539.60.0.0; access_token={self.token}",
            "origin": "https://web.bale.ai",
            "sec-ch-ua": "'Google Chrome';v='111', 'Not(A:Brand';v='8', 'Chromium';v='111'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-grpc-web": "1",
            "x-user-agent": "grpc-web-javascript/0.1"
        }

        return requests.post(url='https://next-api.bale.ai/bale.messaging.v2.Messaging/DeleteMessage',
                      data=data, headers=send_message_headers).text
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
