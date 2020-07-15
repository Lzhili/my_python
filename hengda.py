# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 09:06:22 2020

@author: Lzhili
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
import requests

browser = webdriver.Firefox()
wait = WebDriverWait(browser, 20)

def browse_html(num):
    browser.get('https://www.evergrande.com/Business/Index')
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#more')))
    for i in range(num):
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#more')))                                                
        button.click()                                               
    html = browser.page_source
    return html

def get_information(html):
    doc =pq(html)
    items = doc('.pagelist div').items()
    for item in items:
        name = item.find('p').text()
        pic_url = item.find('img').attr('src')
        save_file(name, pic_url)

def save_file(name, pic_url):
    try:
        r = requests.get(pic_url)
        r.raise_for_status()
        address = name + '.jpg'
        with open('picture\\' + address, 'wb') as f:
            f.write(r.content)
    except:
        print('false')
        
def main():
    num = 10
    html = browse_html(num)
    get_information(html)
    print('图片保存好')

main()        
