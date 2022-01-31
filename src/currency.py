from typing import Text
import requests;
from bs4 import BeautifulSoup;
import copy
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

res = requests.get('https://en.wikipedia.org/wiki/ISO_4217')
soup = BeautifulSoup(res.text, 'html.parser')
table = soup.select('.wikitable')

dic = {}
for tr in table[0].select('tr'):
    td1 = tr.select('td:nth-child(1)')
    td3 = tr.select('td:nth-child(3)')
    td4 = tr.select('td:nth-child(4)')
    for cell1, cell2, cell3 in zip(td1, td3, td4):
        dic[re.sub(r'[^A-Z]', '', cell1.text)] = {'name' : cell3.text, 'name_ko' : '', 'name_local': cell3.text, 'minor_units' : re.sub(r'[^0-9]', '', cell2.text)}



res = requests.get('https://ko.wikipedia.org/wiki/ISO_4217')
soup = BeautifulSoup(res.text, 'html.parser')
table = soup.select('.wikitable')
for tr in table[0].select('tr'):
    td1 = tr.select('td:nth-child(1)')
    td4 = tr.select('td:nth-child(4)')
    for cell1, cell2 in zip(td1, td4):
        if re.sub(r'[^A-Z]', '', cell1.text) in dic:
            dic[re.sub(r'[^A-Z]', '', cell1.text)]['name_ko'] = cell2.text


drv = webdriver.Chrome('./chromedriver')
wait_drv = WebDriverWait(drv, 10)

drv.get('https://en.wikipedia.org/wiki/ISO_4217')

tables = drv.find_elements_by_css_selector(f'.wikitable')
td_list = tables[0].find_elements_by_css_selector('td:nth-child(4)')

td_cnt = len(td_list)
li = []
for i in range(td_cnt):
    tables = drv.find_elements_by_css_selector(f'.wikitable')
    td1 = tables[0].find_elements_by_css_selector(f'td:nth-child(1)')[i]
    td4 = tables[0].find_elements_by_css_selector(f'td:nth-child(4)')[i]
    code = re.sub(r'[^A-Z]', '', td1.text)
    a = td4.find_elements_by_css_selector('a')
    if 0 == len(a): continue
    a[0].click()
    headers = drv.find_elements_by_css_selector(f'.infobox-subheader')
    print(code)
    if 0 < len(headers):
        if code in dic:
            dic[code]['name_local'] = headers[0].text

    # swifts = drv.find_elements_by_css_selector('td.table-swift')
    # names = drv.find_elements_by_css_selector('td.table-name')
    # for name, swift in zip(names, swifts):
    #     li.append({'name' : name.text, 'swift_code' : swift.text})
    #     count += 1
    #     if count == 10000:
    #         bank_lists.append(li)
    #         count = 0
    #         li = []

    drv.get('https://en.wikipedia.org/wiki/ISO_4217')


drv.quit()

print(dic)