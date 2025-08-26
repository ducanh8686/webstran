from time import sleep
import random
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import sqlite3
import asyncio
from playwright_stealth import Stealth
from playwright.async_api import async_playwright
from fake_useragent import UserAgent


#select tu dien trong database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM hanviet")
rows = cursor.fetchall()
dict_hv = dict((row[0], " " + row[1] + " ") for row in rows)
conn.close()

#select tu dien trong database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM hanviet")
rows = cursor.fetchall()
dict_hv = dict((row[0], " " + row[1] + " ") for row in rows)
conn.close()

def rotate_user_agent():
    ua = UserAgent()
    return ua.random

async def scrape_page():
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=False) # Set headless=False to see the browser
        context = await browser.new_context(user_agent=rotate_user_agent())
        page = await context.new_page()
        await page.goto("https://www.69shuba.com/book/30069/", timeout=60000)

        # Get the HTML content after the page has loaded and rendered
        html_content = await page.content()

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        root = etree.fromstring(str(soup), etree.HTMLParser())
        links = root.xpath("//div[@id='catalog']//ul/li/a/@href")
        await browser.close()

        # Example: Extract all paragraph texts
        for p_tag in links:
            sub_link = re.sub(r"https://www.69shuba.com/txt/30069/","", p_tag)
            if int(sub_link) > 22450271:
                await scrape_detail_page(p_tag)
                sleep(2)


async def scrape_detail_page(url):
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=False) # Set headless=False to see the browser
        context = await browser.new_context(user_agent=rotate_user_agent())
        page = await context.new_page()
        await page.goto(url, timeout=60000)
        await asyncio.sleep(10)
        await random_scroll(page, num_scrolls=10, max_scroll_height=700)

        # Get the HTML content after the page has loaded and rendered
        html_content = await page.content()

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
        # sleep(3)
        # print(content)
        await asyncio.sleep(3)
        await browser.close()

async def random_scroll(page, num_scrolls=5, max_scroll_height=500):
    for _ in range(num_scrolls):
        scroll_amount = random.randint(50, max_scroll_height)
        scroll_direction = random.choice([-1, 1])  # -1 for up, 1 for down

        # Scroll by the random amount in a random direction
        await page.evaluate(f"window.scrollBy(0, {scroll_amount * scroll_direction});")
        await asyncio.sleep(random.uniform(0.5, 2))  # Pause for a random duration

if __name__ == "__main__":
    asyncio.run(scrape_page())
