from time import sleep
import requests
import bs4
from lxml import etree
import re
import sqlite3

#select tu dien trong database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM hanviet")
rows = cursor.fetchall()
dict_hv = dict((row[0], " " + row[1] + " ") for row in rows)
conn.close()

url = "https://tw.mingzw.net/mzwchapter/41936.html"  # Replace with the desired URL
response = requests.get(url)

soup = bs4.BeautifulSoup(response.text,"lxml")
root = etree.fromstring(str(soup), etree.HTMLParser())
links = root.xpath("//div[@class='wrap']//ul[@class='gclearfix']/li/a/@href")
list_urls = []
for p in links:
    if '41936_'in p:
        newp= 'https://tw.mingzw.net' + p
        list_urls.append(newp)
head_html = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title></title>
</head>

<body>
"""


foot_html = """
</body>
</html>
"""
# index = 715
# for url in list_urls:
#     url = list_urls[index]
#     index += 1
#     print(url)
for i in range(715,len(list_urls),1): # Start index from 1
    url = list_urls[i]
    print(url)