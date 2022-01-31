from typing import Text
import requests;
from bs4 import BeautifulSoup;
import copy
import re

from requests import api

p = re.compile(r'[A-Z]')

res = requests.get('https://en.wikipedia.org/wiki/List_of_country_calling_codes')
soup = BeautifulSoup(res.text, 'html.parser')
table = soup.select('.wikitable')

di = {}
litmp = []
for tr in table[0].select('tr'):
    for td in tr.select('td'):
        for a in td.select('a'):
            if p.match(a.text):
                if a.text not in di:
                    di[a.text] = []
                di[a.text].append(litmp[-1].replace(' ', ''))
            else :
                litmp.append(a.text)

res = requests.get('https://ko.wikipedia.org/wiki/ISO_3166-1')
soup = BeautifulSoup(res.text, 'html.parser')
table = soup.select('.wikitable')

li = []
for tr in table[0].select('tr'):
    td1 = tr.select('td:nth-child(1)')
    td3 = tr.select('td:nth-child(3)')
    td4 = tr.select('td:nth-child(4)')
    for cell1, cell2, cell3 in zip(td1,td3,td4):
        alpha2_code = cell3.text.replace('\n', '')
        if alpha2_code in di:
            li.append({'alpha2_code': alpha2_code, 'phone_country_code': di[alpha2_code]})

print(li)