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
        page.goto(url)

        # Get the HTML content after the page has loaded and rendered
        html_content = page.content()

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        root = etree.fromstring(str(soup), etree.HTMLParser())
        links = root.xpath("//div[@id='catalog']//ul/li/a/@href")

        # Example: Extract all paragraph texts
        for p_tag in links:
            print(p_tag)

        browser.close()

if __name__ == "__main__":
    target_url = "https://www.69shuba.com/book/30069/" # Replace with your target URL
    scrape_page(target_url)
