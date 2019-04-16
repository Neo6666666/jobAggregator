# import requests
import codecs
import time
import re

from selenium import webdriver
from bs4 import BeautifulSoup as bs


# session = requests.Session()
# headers = {
#   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) /
#                  Gecko/20100101 Firefox/65.', 
#   'Accept': 'text/html,application/xhtml+xml,/
#             application/xml;q=0.9,image/webp,*/*;q=0.8'}

jobs = []
pages = []
domain = 'https://job42.ru'

url = 'https://job42.ru/vacancy/it-i-internet'  #'https://job42.ru/vacancy/programmist-java'
pages.append(url)
web_drv = webdriver.Firefox()
web_drv.get(url)
time.sleep(10)
data = web_drv.page_source
last_tag = re.findall(re.compile('vacancy-item_*.{5}'), str(data))[0]

bs_obj = bs(data, 'html.parser')

pagination = bs_obj.find_all('a', attrs={
                            'class': 'ui button item floated left page-item'
                            })
if pagination:
    for page in pagination:
        pages.append(domain + page['href'])

for page in pages:
    divs = bs_obj.find_all('div', attrs={'class': 'ui segment ' + last_tag})
    if divs:
        for div in divs:
            jobs.append({
                'text': div.a.text,
                'link': domain + div.a['href']
            })


data = bs_obj.prettify()
file_handle = codecs.open('job42.html', 'w', 'utf-8')
file_handle.write(str(jobs))
file_handle.close()
