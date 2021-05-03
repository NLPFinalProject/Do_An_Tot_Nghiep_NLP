from googlesearch import search
import requests
import os
import preprocessor as p
from urllib.request import urlopen
from bs4 import BeautifulSoup
from ScrapeSearchEngine.ScrapeSearchEngine import Google
from ScrapeSearchEngine.ScrapeSearchEngine import Duckduckgo
from ScrapeSearchEngine.ScrapeSearchEngine import Givewater
from ScrapeSearchEngine.ScrapeSearchEngine import Bing
from ScrapeSearchEngine.ScrapeSearchEngine import Yahoo
from ScrapeSearchEngine.ScrapeSearchEngine import Ecosia

userAgent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
             ' Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68')
#search on google "my user agent"

#check a url can be doawnloaded as a file?
def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True
# search keyword from multiple search engine include
def search_keyword(search):
    list_url = []
    list_url.extend(Google(search, userAgent))
    list_url.extend(Bing(search, userAgent))
    list_url.extend( Yahoo(search, userAgent))
    list_url.extend(Duckduckgo(search, userAgent))
    list_url.extend(Givewater(search, userAgent))
    list_url.extend (Ecosia(search, userAgent))
    return list(dict.fromkeys(list_url))

# download file downloadable such as: pdf, docx,...
def download_document(url):
    if (is_downloadable(url)):
        name = os.path.basename(url)
        r = requests.get(url, allow_redirects=True)
        open("file_downloaded\\" + name, 'wb').write(r.content)
        return "file_downloaded\\" + name

# crawl text from html website then preprocess and give output: list sentence after preprocessing.
def crawl_web(url):
    html = urlopen(url).read()
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
    temp = p.list_para2txt(text.split("\n"))
    res  = p.convert2listsentence(temp)
    return res #list sentence