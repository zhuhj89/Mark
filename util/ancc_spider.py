# -*- coding: utf-8 -*-
"""
  the Approve Management ws interface
"""
__author__ = "zhuihuijie"
__email__ = "zhuihuijie@cnnic.cn"
__copyright__ = "Copyright 2014, Cnnic"
__version__ = "1.0.0"
__deprecated__ = False
__date__ = "2014-8-26"

import urllib
import urllib2
from bs4 import BeautifulSoup
import re


def get_viewstate(webdata):
    result = re.compile(r'__VIEWSTATE.*value=".*"').findall(webdata)
    result = re.compile(r'value=".*"').findall(result[0])
    result = result[0].split('"')[1]
    return result


def get_eventvalidation(webdata):
    result=re.compile(r'__EVENTVALIDATION.*value=".*"').findall(webdata)
    result=re.compile(r'value=".*"').findall(result[0])
    result=result[0].split('"')[1]
    return result


def make_request(opener,url,eventargument,eventtarget,viewstate,eventvalidation,keyword):
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    #"Referer": "",
    "Accept-Language": "zh-cn",
    "Content-Type": "application/x-www-form-urlencoded",
    #"Accept-Encoding": "gzip, deflate",
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
    "Connection": "Keep-Alive",
    "Cache-Control": "no-cache",
        "Referer":	"http://ancc.org.cn/Service/queryTools/Internal.aspx",
        "Cookie":	"ANCC_2013_Revision_Notice=1; ASP.NET_SessionId=tj3ygr45qw32bczvm4nliaag"
    }

    body = {
        '__EVENTTARGET':eventtarget,
    '__VIEWSTATE':viewstate,
    '__EVENTVALIDATION':eventvalidation,


    '__EVENTARGUMENT':eventargument,
    'query-condition':'RadioItemOwnership',
    'query-supplier-condition':'Radio1',
    'subjoin':'4444',
        'btn_query':'查询',
    'txtcode':keyword
    }

    request = urllib2.Request(url=url,data=urllib.urlencode(body),headers=headers)
    data=urllib.urlencode(body)
    #print 'ecoded url data:',data
    response = opener.open(request)
    print response.info()
    content = response.read()
    return content


def company_prefix_info(company_prefix):

    url = 'http://ancc.org.cn/Service/queryTools/Internal.aspx'
    webdata = urllib.urlopen(url).read()
    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    urllib2.install_opener(opener)
    eventtarget = ''
    eventargument = ''
    viewstate=get_viewstate(webdata)
    eventvalidation = get_eventvalidation(webdata)
    webdata=make_request(opener,url,eventargument,eventtarget,viewstate,eventvalidation,company_prefix)
    soup = BeautifulSoup(webdata)
    result_data = soup.select('div[id="searchResult"]')[0]
    # result_head = result_data.find_all('th')
    result_body = result_data.find_all('td')
    result = {}
    if result_body:
        result = {'company_rrid': result_body[0].text, 'company_name': result_body[1].text}
        if result_body[2].text == u'有效':
            return [1, result]
        else:
            return [2, result]
    else:
        return [0, None]

if __name__ == '__main__':
    r = company_prefix_info('69328601')
    print r
    print r[1]['company_name'].encode('gbk')
    