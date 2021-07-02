import os
from urllib.request import urlopen, Request

import requests
from ScrapeSearchEngine.ScrapeSearchEngine import Google, Duckduckgo, Givewater, Bing, Yahoo
from bs4 import BeautifulSoup
from django.conf import settings

import PreprocessingComponent.views as p

userAgent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
             ' Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68')


# search on google "my user agent"
# check a url can be doawnloaded as a file?
def IsDownloadable(url):
    """
    Does the url contain a downloadable resource
    """
    try:
        h = requests.head(url, allow_redirects=True)
        header = h.headers
        contentType = header.get('content-type')
        if 'text' in contentType.lower():
            return False
        if 'html' in contentType.lower():
            return False
        return True
    except:
        return False


def SearchKeyword(search):
    listUrl = []
    try:
        listUrl.extend(Google(search, userAgent))
    except:
        pass
    try:
        listUrl.extend(Bing(search, userAgent))
    except:
        pass
    try:
        listUrl.extend(Yahoo(search, userAgent))
    except:
        pass
    try:
        listUrl.extend(Duckduckgo(search, userAgent))
    except:
        pass
    try:
        listUrl.extend(Givewater(search, userAgent))
    except:
        pass
    return list(dict.fromkeys(listUrl))


# download file downloadable such as: pdf, docx,...
def DownloadDocument(url):
    if (IsDownloadable(url)):
        name = os.path.basename(url)
        r = requests.get(url, allow_redirects=True)
        f = open(settings.MEDIA_ROOT + '\\DocumentFile\\file_downloaded\\' + name, 'wb')
        f.write(r.content)
        return settings.MEDIA_ROOT + '\\DocumentFile\\file_downloaded\\' + name


# crawl text from html website then preprocess and give output: list sentence after preprocessing.
def CrawlWeb(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68'}
        req = Request(url, headers=headers)
        html = urlopen(req).read()
        soup = BeautifulSoup(html, features="html.parser")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out
        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        temp = text.split("\n")
        lstSentecne = p.ListSentence(temp)
        temp1 = p.SplitSenList(lstSentecne, 450)
        res = [sen.replace("\xa0", "") for sen in temp1]
        return res  # list sentence
    except:
        return None
