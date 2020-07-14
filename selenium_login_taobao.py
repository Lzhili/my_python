# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 15:05:44 2020

@author: Lzhili
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from tqdm import tqdm
from time import sleep
import json

goods = input('请输入要搜索的商品:')
last_page = int(input('要爬取的页数:'))
browser = webdriver.Firefox()
wait = WebDriverWait(browser, 20)

def login_taobao_and_search(goods):
    browser.get('https://www.taobao.com')
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.site-nav-sign > a:nth-child(1)')))
    login_button.click()
    scan = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.icon-qrcode')))
    scan.click()
    search_frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
    search_frame.send_keys(goods)
    search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))
    search_button.click() 

def get_base_html(page):   
    if page > 1:
        input_page_frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.input:nth-child(2)')))
        input_page_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.btn:nth-child(4)')))
        input_page_frame.clear()
        input_page_frame.send_keys(page)
        input_page_button.click()    
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))    
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))    
    return browser.page_source
    
def get_message(base_html):
    doc = pq(base_html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
                'price': item.find('.price').text(),
                'deal': item.find('.deal-cnt').text(),
                'title': item.find('.title').text(),
                'shop': item.find('.shop').text(),
                'location': item.find('.location').text(),
                
                }
        save_file(product)
        
def save_file(product):
    with open('r.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(product, indent=2, ensure_ascii=False))        
    
def main():
    login_taobao_and_search(goods)
    for page in range(1, last_page + 1):
        print('正在爬取第',page,'页')   
        base_html = get_base_html(page)
        get_message(base_html)
        for i in tqdm(range(100)):
            sleep(0.02) 
        print('第',page,'页爬取完成')
    browser.close()    
    print('数据以储存在json文件')    

main()    
