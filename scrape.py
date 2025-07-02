from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os

def scrape_website(website):
    print("🚀 Launching local Chrome...")

    # Set up the local ChromeDriver path
    chrome_driver_path = "./chromedriver"  # Make sure chromedriver is in your project folder

    options = Options()
    options.add_argument("--headless")  # Comment this line if you want to see the browser
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website)
        print("✅ Page loaded successfully")
        html = driver.page_source
        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    print("⚠️ No <body> tag found. Returning entire HTML.")
    return str(soup)

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for tag in soup(["script", "style"]):
        tag.extract()

    cleaned = soup.get_text(separator="\n")
    return "\n".join(line.strip() for line in cleaned.splitlines() if line.strip())

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i: i + max_length]
        for i in range(0, len(dom_content), max_length)
    ]
