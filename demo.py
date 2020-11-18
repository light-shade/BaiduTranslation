import execjs
import re
import requests


session = requests.session()
cookies_str = ''
cookies = {}
cookies_str = cookies_str.split(';')
for cookie_str in cookies_str:
    cookie_str = cookie_str.strip()
    key, value = cookie_str.split('=', 1)
    cookies[key] = value

session.cookies.update(cookies)


def get_sign(gtk, string):
    with open('index.js', encoding='utf-8') as f:
        content = f.read()
    ctx = execjs.compile(content, cwd=r'C:\Users\qh\node_modules')
    sign = ctx.call('e', string, gtk)
    print(sign)
    return sign


def token_text():
    resp = session.get('https://fanyi.baidu.com/')
    resp.encoding = resp.apparent_encoding
    token = re.findall("token: '(.*?)',", resp.text, re.S)[0]
    gtk = re.findall("window.gtk = '(.*?)';", resp.text)[0]
    print(token)
    return token, gtk


def translate(string):
    token, gtk = token_text()
    sign = get_sign(gtk, string)
    api = 'https://fanyi.baidu.com/v2transapi?'
    headers = {
        'x-requested-with': 'XMLHttpRequest'
    }
    session.headers.update(headers)
    params = {
        'from': 'zh',
        'to': 'en',
    }
    data = {
        'from': 'zh',
        'to': 'en',
        'query': string,
        'simple_means_flag': '3',
        'sign': sign,
        'token': token,
        'domain': 'common',
    }
    resp = session.post(api, params=params, headers=headers, data=data).json()
    print(resp)

if __name__ == '__main__':
    translate('爷爷')
