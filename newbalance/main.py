from bs4 import BeautifulSoup
import urllib.request
import http.cookiejar
import json
import datetime
from urllib.request import Request, urlopen

def handler(event, context):
    username = event['account']['username']
    password = event['account']['password']

    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj),
        urllib.request.HTTPRedirectHandler(),
        urllib.request.HTTPHandler())
    opener.addheaders = [('User-agent', "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36")]
    postdata = json.dumps({"name":username,"password":password}).encode("utf-8")

    req = Request('https://www.twino.eu/ws/public/login',
                headers={'Content-Type': 'application/json;charset=UTF-8'},
                data=postdata,
                method='POST')

    response = opener.open(req)
    html = response.read()

    req = Request('https://www.twino.eu/ws/web/investor/my-account-summary',
      headers={'accept': 'application/json, text/plain, */*'},
      method='GET')

    html = opener.open(req).read()
    print(html)
    result = json.loads(html);

    resultStr = json.dumps(result)
    customcontext = context.client_context.custom
    if "lastvalue" in customcontext and resultStr == customcontext['lastvalue']:
      return
    else:
      result['dedupid']=resultStr
      return result
