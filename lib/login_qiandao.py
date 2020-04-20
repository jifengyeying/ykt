import requests
from . import pwd


def cookie_str_to_dict(cookie_str):
    cookie_dict=  {}
    list_ = cookie_str.split(';') if cookie_str.find('; ') == -1 else cookie_str.split('; ')
    for i in list_:
        cookie_dict.update({i.split('=')[0]:i.split('=')[1]})
    return cookie_dict

def cookie_dict_to_str(cookie_dict):
    cookie_str = ''
    for i in cookie_dict.keys():
        cookie_str += i+'='+cookie_dict.get(i)+'; '
    return cookie_str[:-2]

def login(user, password):
    login_dict = {'account': '', 'password': '', 'ipForget':'true'}
    login_dict['account'] = user
    login_dict['password'] = pwd.encrypt(password)
    headers = {'Host': 'ykt.zenking.cc', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Referer': '', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'Cookie': ''}
    login_headers = requests.post(url='http://ykt.zenking.cc/user/ajax/login', data=login_dict, headers=headers).headers
    if not login_headers.get('Set-Cookie'):
        return None
    result = 'SESSION='+requests.post('http://ykt.zenking.cc/dialog/ajax/loginReg').headers['Set-Cookie'].split(';')[0].split('=')[1]+';'
    for i in login_headers.get('Set-Cookie').split(' Expires='):
        for j in i.split('Path=/, '):
            if not j.endswith(' '):
                if not j.endswith('/'):
                    result += j
    if result.endswith(';'):
        result = result[:-1]
    result_dict = cookie_str_to_dict(result)
    result_dict['web_user_logindatatime'] = result_dict['web_user_logindatatimeinxedu_customer_chanjing']
    result = cookie_dict_to_str(result_dict)

    return result

def qiandao():
    pass

def cookie_change_test():
    cookie = 'WEB_USER_LOGIN_PREFIXinxedu_customer_chanjing=26b450e86dcf4a54baf5fd1f562373a9; web_user_logindatatimeinxedu_customer_chanjing=2020-04-17%2019%3A22%3A27; web_user_logindatatime=2020-04-17%2019%3A22%3A27; courseIdinxedu_customer_chanjing=193; SESSION=MTZhZTIxOTAtM2Y5Ni00MzNlLWE4M2MtZTZmZjJiODBlZjIx; ONLINE_NUMBERinxedu_customer_chanjing=WEB_LOGINER29b023416f3f4963a533474ce6fc948c; s=1587259307570'
    print('Yes') if cookie == cookie_dict_to_str(cookie_str_to_dict(cookie)) else print('No')
