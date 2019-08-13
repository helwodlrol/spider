import os
import requests
from bs4 import BeautifulSoup

def get_content(url):
    r = requests.get(url, headers=headers)
    r.encoding='utf-8'
    bs = BeautifulSoup(r.text, 'lxml')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
base_url = 'https://m.48wx.org'
r = requests.get('%s/4_4839/all.html' % base_url, headers = headers)
r.encoding='utf-8'
soup = BeautifulSoup(r.text, 'lxml')
content = soup.find_all('p')
f = open(os.path.join(os.getcwd(), 'zyx.txt'), 'w')
for p in content:
    a = p.a
    if a and '4_4839' in a.get('href'):
        page = a.get('href')
        r_page = requests.get(base_url+page, headers=headers)
        r_page.encoding='utf-8'
        bs = BeautifulSoup(r_page.text, 'lxml')
        chapter = bs.find('div', id='chaptercontent')
        chaptercontent = chapter.get_text().replace('<br/>', '\n')
        chaptercontent = chaptercontent[:chaptercontent.find('-->>')].strip()

        a_page = bs.find_all('p', 'Readpage')[-1].find('a', id='pt_next')
        while '下一页' == a_page.get_text():
            next = base_url+a_page.get('href')
            next_page = requests.get(next, headers=headers)
            next_page.encoding='utf-8'
            next_bs = BeautifulSoup(next_page.text, 'lxml')
            next_chapter = next_bs.find('div', id='chaptercontent').get_text().replace('<br/>', '\n')
            if '-->>' in next_chapter:
                next_chapter = next_chapter[:next_chapter.find('-->>')]
            chaptercontent += next_chapter.strip()
            a_page = next_bs.find_all('p', class_='Readpage')[-1].find('a', id='pt_next')
        f.write('\n\n' + a.get_text() + '\n\n' + chaptercontent[:chaptercontent.rfind('\')')])
f.close()
