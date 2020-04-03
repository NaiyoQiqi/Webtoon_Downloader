import json
import time
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup as bs4

import module.shared as shared
from module.makeurl import makeRootUrl, makeUrl


def getRootHtmlWorker(op, webtoonId, cookie):
    if cookie != None:
        if op == 'naver':
            cookies = {'NID_AUT': cookie._auth, 'NID_SES': cookie._sess}
        if op == 'daum':
            cookies = {'HM_CU': cookie._hm_cu, 'HTS': cookie._hts, 'PROF': cookie._prof, 'TS': cookie._ts,
                       'LSID': cookie._lsid}
    else:
        cookies = None
    try:
        t = requests.get(makeRootUrl(op, webtoonId), cookies=cookies).text
    except:
        t = -1
    return t


def getRootHtml(op, webtoonId, cookie):
    if shared.rootHtml != None:
        return shared.rootHtml
    while True:
        td = getRootHtmlWorker(op, webtoonId, cookie)
        if td == -1:
            time.sleep(0.5)
            continue
        shared.rootHtml = td
        return td


def getRawHtmlWorker(op, webtoonId, cookie, viewNo=0):
    cookies = dict()
    if cookie != None:
        if op == 'naver':
            cookies = {'NID_AUT': cookie._auth, 'NID_SES': cookie._sess}
        if op == 'daum':
            cookies = {'HM_CU': cookie._hm_cu, 'HTS': cookie._hts, 'PROF': cookie._prof, 'TS': cookie._ts,
                       'LSID': cookie._lsid}
    else:
        cookies = None
    try:
        t = requests.get(makeUrl(op, webtoonId, viewNo), cookies=cookies).text
    except:
        t = -1
    return t


def getRawHtml(op, webtoonId, cookie, viewNo=0):
    if viewNo == -1:
        return -1
    while True:
        td = getRawHtmlWorker(op, webtoonId, cookie, viewNo)
        if td == -1:
            time.sleep(0.5)
            continue
        return td


def getHtml(op, webtoonId, viewNo, cookie):
    if op == 'naver' or op == 'nbest' or op == 'nchall':
        for findFor in range(len(shared.reIndex), viewNo + 2):
            for i in range(shared.reIndex[findFor - 1] + 1, int(getFinCode(op, webtoonId, cookie)) + 2):
                tmpHtml = getRawHtml(op, webtoonId, cookie, i)
                if getRawEpisodeNo(tmpHtml) == str(i):
                    shared.reIndex.append(i)
                    shared.html.update({len(shared.reIndex) - 1: tmpHtml})
                    break
        return shared.html[viewNo]
    if op == 'daum':
        if shared.htmlLst == None:
            shared.htmlLst = list()
            t = getRootHtml(op, webtoonId, cookie)
            js = json.loads(t)
            webtoonLinks = js['data']['webtoon']['webtoonEpisodes']
            lst = list()
            lst.append(-1)
            for i in webtoonLinks:
                if i['serviceType'] == 'free' or i['isPaid']:
                    lst.append(i['articleId'])
                else:
                    lst.append(-1)
            for i in lst:
                if i == -1:
                    shared.htmlLst.append(-1)
                    continue
                try:
                    t = getRawHtml(op, i, cookie)
                except:
                    t = -1
                shared.htmlLst.append(t)
        return shared.htmlLst[int(viewNo)]


def getRawEpisodeNo(html):
    soup = bs4(html, 'html.parser')
    try:
        return parse_qs(urlparse(soup.find('meta', {"property": "og:url"})['content']).query)['no'][0]
    except:
        return -1


def getFinCode(op, webtoonId, cookie):
    if shared.fincode != None:
        return shared.fincode
    fincode = getRawEpisodeNo(getRawHtml(op, webtoonId, cookie, 0))
    return fincode
