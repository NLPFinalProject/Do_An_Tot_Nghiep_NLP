from googlesearch import search
import requests
import os

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

def search_keyword(keyword):
	list_url=[]
	for url in search(keyword):
	    list_url.append(url)
	return list_url


def download_pdf(list_url):
	for url in list_url:
	    if(".pdf" in url):
	    	if(is_downloadable(url)):
		        name=os.path.basename(url)
		        r = requests.get(url, allow_redirects=True)
		        open("file_downloaded\\"+name, 'wb').write(r.content)

