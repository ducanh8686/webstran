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

url = "https://tw.mingzw.net/mzwread/41936_11962386.html"  # Replace with the desired URL
response = requests.get(url)

soup = bs4.BeautifulSoup(response.text,"lxml")
#root = etree.fromstring(str(soup), etree.HTMLParser())
#links = root.xpath("//div[@class='wrap']//ul[@class='gclearfix']/li/a/@href")
my_div = soup.find("div", {"class": "contents"})
my_ps = my_div.find_all('div')
for my_p in my_ps:
    my_p.decompose()
newcontent = my_div.decode_contents().strip()
newcontent = re.sub(r"第([^第<]+?)章([^第<]+)\←([^第<]+)","",newcontent)
newcontent = re.sub(r"(mayiwsk([^<]+|)|)←([^<]+)明智屋中文([^<]+)","",newcontent)
newcontent = newcontent.replace("<p>","ptagopen")
newcontent = newcontent.replace("</p>","<p>")
newcontent = newcontent.replace("ptagopen","</p>")
if not newcontent.startswith("<p>"):
    newcontent = "<p>" + newcontent
if not newcontent.endswith("</p>"):
    newcontent = newcontent + "</p>"


my_div_top = soup.find("div", {"class": "novel-top2"})
my_ps_top = my_div_top.find_all('div')
for my_p_top in my_ps_top:
    my_p_top.decompose()
content_top = my_div_top.text.strip().replace(" ","").replace("普羅之主-","")
if content_top in newcontent:
    total_content = newcontent
else:
    head_top_p = """<p>"""
    foot_top_p = """</p>
    """
    total_content = head_top_p + content_top + foot_top_p + newcontent
#for my_p in my_ps:
#    print(my_p)

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
all_html = head_html + total_content + foot_html
replreplacements = str.maketrans(dict_hv)
new_all_html= all_html.translate(replreplacements)
#new_all_html = new_all_html.replace("  "," ")
new_all_html = re.sub(r"  "," ", new_all_html)
new_all_html = re.sub(r" ！","!", new_all_html)
new_all_html = re.sub(r" ，",",", new_all_html)
new_all_html = re.sub(r" \？","?", new_all_html)
new_all_html = re.sub(r"。",".", new_all_html)
new_all_html = re.sub(r" \.",".", new_all_html)
new_all_html = re.sub(r'”“','” “', new_all_html)

#print(new_all_html)
with open('41936_11962286.html', "w", encoding="utf-8") as file:
    file.write(new_all_html)