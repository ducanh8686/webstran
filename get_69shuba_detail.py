from time import sleep
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import sqlite3
from playwright.sync_api import sync_playwright


#select tu dien trong database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM hanviet")
rows = cursor.fetchall()
dict_hv = dict((row[0], " " + row[1] + " ") for row in rows)
conn.close()

def scrape_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Set headless=False to see the browser
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')

        # Get the HTML content after the page has loaded and rendered
        html_content = page.content()

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        root = etree.fromstring(str(soup), etree.HTMLParser())
        content = soup.find("div", {"class": "txtnav"})

        #loai bo the div ben trong content
        div_tags = content.find_all("div")
        for div_tag in div_tags:
            div_tag.decompose()

        #loai bo the h1 ben trong content
        h1_tags = content.find_all("h1")
        for h1_tag in h1_tags:
            h1_tag.decompose()
        
        head_html = """<?xml version="1.0" encoding="utf-8"?>
            <!DOCTYPE html>

            <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
            <head>
            <title></title>
            </head>

            <body>
            <p>"""


        foot_html = """
        </body>
        </html>
        """
        content = content.decode_contents().strip()
        content = re.sub("<br/><br/>", "</p><p>", content)
        content = re.sub(r'\n', "", content)
        content = content.replace("\u2003", " ")
        content = re.sub("<p>    ", "<p>", content)
        content = re.sub("<p>   ", "<p>", content)
        content = re.sub("<p>  ", "<p>", content)
        content = re.sub("<p> ", "<p>", content)
        index = content.rfind("</p><p>")
        if index == -1:
            content = content
        else:
            content = content[:index] + "</p>" + content[index + len("</p><p>"):]
        all_html = head_html + content + foot_html
        replreplacements = str.maketrans(dict_hv)
        new_all_html= all_html.translate(replreplacements)
        file_name = re.sub(r"https://www.69shuba.com/txt/30069/","", url) + ".xhtml"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(new_all_html)
        sleep(3)
        # print(content)

        browser.close()

if __name__ == "__main__":
    target_url = "https://www.69shuba.com/txt/30069/25726167" # Replace with your target URL
    scrape_page(target_url)