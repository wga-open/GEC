# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
import json
from hashlib import md5

# Set your own appid/appkey.
appid = '20220622001254827'
appkey = 'MAYwJuwNQs3NAnqfW80a'

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
def createRequest(query,from_lang,to_lang,):


    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    # query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'

    # Generate salt and sign
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    sol=[i['dst'] for i in result['trans_result']]
    # print(sol)
    return sol

# Show response
if __name__ == '__main__':
    pass
    # print(json.dumps(result, indent=4, ensure_ascii=False))
    # for i in result['trans_result']:
    #     print(i['dst'])
# print(result['trans_result'])
