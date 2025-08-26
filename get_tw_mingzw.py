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

for i in range(715,len(list_urls),1): 
    urlnew = list_urls[i]
    file_name = re.sub(r"https://tw.mingzw.net/mzwread/","", urlnew)
    responsenew = requests.get(urlnew)
    soupnew = bs4.BeautifulSoup(responsenew.text,"lxml")
    my_div = soupnew.find("div", {"class": "contents"})
    my_p = my_div.find_all('p')
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
    
    my_div_top = soupnew.find("div", {"class": "novel-top2"})
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
    
    all_html = head_html + total_content + foot_html
    replreplacements = str.maketrans(dict_hv)
    new_all_html= all_html.translate(replreplacements)
    new_all_html = re.sub(r"  "," ", new_all_html)
    new_all_html = re.sub(r" ！","!", new_all_html)
    new_all_html = re.sub(r" ，",",", new_all_html)
    new_all_html = re.sub(r" \？","?", new_all_html)
    new_all_html = re.sub(r"。",".", new_all_html)
    new_all_html = re.sub(r" \.",".", new_all_html)
    new_all_html = re.sub(r'”“','” “', new_all_html)
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(new_all_html)
    sleep(3)


#sleep(50)

# output_filename = "index.html" # Name of the file to save the HTML

# try:
#     response = requests.get(url)
#     response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

#     with open(output_filename, "w", encoding="utf-8") as file:
#         file.write(response.text)

#     print(f"HTML content successfully saved to {output_filename}")

# except requests.exceptions.RequestException as e:
#     print(f"An error occurred: {e}")