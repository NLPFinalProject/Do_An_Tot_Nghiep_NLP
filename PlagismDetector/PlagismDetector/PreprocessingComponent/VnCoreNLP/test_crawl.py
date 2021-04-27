import requests
from bs4 import BeautifulSoup

news = requests.get("https://vnexpress.net/ly-do-anh-xoay-truc-sang-chau-a-hau-brexit-4256015.html")

soup = BeautifulSoup(news.content, "html.parser")
#print(soup)
title = soup.find("h1").text

body = soup.find("div").text
#content = soup.find_all("p")
content = soup.get_text()

# print(title)

# print(body)
print(content)
print("_________________________________________________________________________")