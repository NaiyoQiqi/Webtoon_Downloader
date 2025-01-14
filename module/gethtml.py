import json
from module.shared import reIndex, html, htmlLst
from module.getraw import getRawHtml, getRawEpisodeNo, getRootHtml
from module.utils import getFinCode

def getHtml(op, webtoonId, viewNo, cookie):
    if op == 'naver' or op == 'nbest' or op == 'nchall':
        while len(reIndex) <= viewNo:
            reIndex.append(-1)
        for findFor in range(len(reIndex), viewNo + 1):
            for i in range(reIndex[findFor - 1] + 1, int(getFinCode(op, webtoonId, cookie)) + 1):
                tmpHtml = getRawHtml(op, webtoonId, cookie, i)
                if getRawEpisodeNo(tmpHtml) == str(i):
                    reIndex.append(i)
                    html[len(reIndex) - 1] = tmpHtml
                    break
        return html.get(viewNo, None)

    elif op == 'kakao':
        if htmlLst is None:
            htmlLst = []
            t = getRootHtml(op, webtoonId, cookie)
            js = json.loads(t)
            webtoonLinks = js.get('singles', [])
            lst = [-1] + [i['id'] for i in webtoonLinks]
            for i in lst:
                if i == -1:
                    htmlLst.append(-1)
                else:
                    try:
                        t = getRawHtml(op, i, cookie)
                    except Exception as e:
                        print(f"Error fetching HTML for Kakao ID {i}: {e}")
                        t = -1
                    htmlLst.append(t)
        return htmlLst[int(viewNo)] if viewNo < len(htmlLst) else None

    elif op == 'another_option':
        print(f"Fetching HTML for Another Option Webtoon ID: {webtoonId}, Episode: {viewNo}")
        return None

    else:
        raise ValueError(f"Unsupported platform: {op}")
