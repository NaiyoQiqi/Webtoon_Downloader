def getHtml(op, webtoonId, viewNo, cookie):
    if op == 'naver' or op == 'nbest' or op == 'nchall':
        while len(shared.reIndex) <= viewNo + 1:
            shared.reIndex.append(-1)  # Ensure reIndex has enough elements.
        for findFor in range(len(shared.reIndex), viewNo + 2):
            for i in range(shared.reIndex[findFor - 1] + 1, int(getFinCode(op, webtoonId, cookie)) + 2):
                tmpHtml = getRawHtml(op, webtoonId, cookie, i)
                if getRawEpisodeNo(tmpHtml) == str(i):
                    shared.reIndex.append(i)
                    shared.html.update({len(shared.reIndex) - 1: tmpHtml})
                    break
        return shared.html[viewNo]
    if op == 'kakao':
        if shared.htmlLst == None:
            shared.htmlLst = list()
            t = getRootHtml(op, webtoonId, cookie)
            js = json.loads(t)
            webtoonLinks = js['singles']
            lst = list()
            lst.append(-1)
            for i in webtoonLinks:
                lst.append(i['id'])
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
