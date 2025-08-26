from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def get_dynamic_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_default_timeout(60000)
        try:
            #page.goto(url, wait_until='networkidle') # Wait for network activity to settle
            page.goto(url, wait_until="load")
            html_content = page.content()
            return html_content
        except Exception as e:
            print(f"Error fetching HTML: {e}")
            return None
        finally:
            browser.close()

# Example usage:
url = "https://www.69shuba.com/" # Replace with your target URL
html = get_dynamic_html(url)
if html:
    print(f"HTML content length: {len(html)} characters")
    # You can now parse 'html' using libraries like BeautifulSoup if needed
    # from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())