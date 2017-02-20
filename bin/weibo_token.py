import urllib2
import urllib
import sys
import json
import os

def get_token(code,file):
    login_data = {
        'client_id': '1539613302',
        'client_secret': '331db01afca70a8f5017bd8921f527c7',
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://107.151.65.204:8080/auth',
    }
    login_data['code'] = code
    login_url = 'https://api.weibo.com/oauth2/access_token'
    login_data = urllib.urlencode(login_data)
    http_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0',
                    }
    req_login = urllib2.Request(
        url=login_url,
        data=login_data,
        headers=http_headers,
    )
    try:
        result = urllib2.urlopen(req_login, timeout=1500)
        print 'open url succeed'
        text = result.read()
        with open(file, 'a+') as fd:
            fd.write(text)
        print (text)
        print 'end of open'
        return True
    except urllib2.URLError:
        print ('ERROR: url open fail')
        e = sys.exc_info()[0]
        print (e)
        return False
def store_token(file, token_store_file):
    with open(file, 'r') as fd:
        js = json.load(fd)
        print (type(js))
        if not os.path.exists(token_store_file):
            with open(token_store_file, 'w+') as fw:
                fw.close()
        if js['access_token']:
            print (js['access_token'])
            with open(token_store_file,'r') as f:
                try:
                    jst = json.load(f)
                    count = 0
                    for i in jst:
                        if i['uid'] == js['uid']:
                            jst.pop(count)
                            jst.append(js)
                            with open(token_store_file, 'w') as ff:
                                json.dump(jst, ff)
                                print ('renew')
                                return
                        count += 1
                except:
                    pass
            with open(token_store_file, 'r') as f:
                try:
                    jst = json.load(f)
                except:
                    jst = []
                jst.append(js)
                with open(token_store_file, 'w') as ff:
                    json.dump(jst, ff)

if __name__ == '__main__':
    store_token('token.db', 'tokens')
    exit(0)
    if not sys.argv or (sys.argv[0]== __file__ and len(sys.argv) < 3 ):
        print ('pass code to this script!')
        exit(1)
    if len(sys.argv) > 2:
        get_token(sys.argv[1])
    else:
        get_token(sys.argv[0])
